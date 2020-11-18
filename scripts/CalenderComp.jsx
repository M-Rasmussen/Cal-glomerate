import React, { useState } from 'react';
import { Calendar, Views, momentLocalizer } from 'react-big-calendar';
import * as dates from './dates';
import moment from 'moment';
import './CalenderStyle.css';
import { Socket } from './Socket';
import { Create_event } from './Add_Event';
import { Modify } from './Modify.jsx';
export function Cal_comp(props) {
  const [events, setEvents] = React.useState([]);
  const localizer = momentLocalizer(moment);
  const [mod,setMod]= React.useState({render: false})
  React.useEffect(() => {
    console.log(events);
    Socket.emit('get events', props.ccode[0]);
    Socket.on('recieve all events', (data) => {
      setEvents(
        data.map((event) => {
          
          let intstart = parseInt(event['start']);
          let start = new Date(intstart * 1000);
          let intend = parseInt(event['end']);
          let end = new Date(intend * 1000);
          let title = event['title'];
          return {
            start,
            end,
            title
          };
        })
      );
    });
  }, []);
  function new_Event() {
    React.useEffect(() => {
      Socket.on('calender_event', (data) => {
        console.log(data);
        console.log('title ' + data['title']);
        console.log('start: ' + data['start']);
        console.log('end: ' + data['end']);
        let intstart = parseInt(data['start']);
        let start = new Date(intstart * 1000);
        let intend = parseInt(data['end']);
        let end = new Date(intend * 1000);
        console.log(end);
        let title = data['title'];
        console.log('ADDING NEW INDIVIDUAL EVENT');
        setEvents((prevEvents) => [...prevEvents, { start, end, title }]);
      });
    }, []);
  }

  new_Event();
  const add = () => {
    setMod({render: false})
  }
  //onSelectEvent={()=> setMod({render: true }) } 
  
 // { mod.render && (<Modify ccode={props.ccode}  />)}
  return (
    <div style={{ height: '100%' }}>
    { mod.render ? <Modify ccode={props.ccode} event={mod.event}  /> :null}
      <Calendar
        //   selectable
        localizer={localizer}
        events={events}
        step={60}
        defaultView={Views.MONTHS}
        max={dates.add(dates.endOf(new Date(2015, 17, 1), 'day'), -1, 'hours')}
        scrollToTime={new Date(1970, 1, 1, 6)}
        defaultDate={new Date(2020, 10, 1)}
          onSelectEvent={event => 
          {
            
            
            setMod({render: true, event })
          }
          
            
          } // add event title here 
        
          
          
        //   onSelectSlot={handleSelect}
      />
      
    </div>
  );
}
