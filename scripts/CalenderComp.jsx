import React, { useState } from 'react';
import { Calendar, Views, momentLocalizer } from 'react-big-calendar';
import * as dates from './dates';
import moment from 'moment';
import './CalenderStyle.css';
import { Socket } from './Socket';
import TimePicker from 'react-time-picker';

import {
  ContextualMenu,
  DatePicker,
  DefaultButton,
  Modal,
  Stack,
  TextField
} from 'office-ui-fabric-react';
import { Card } from '@uifabric/react-cards';




export function Cal_comp(props) {
  const [events, setEvents] = React.useState([]);
  const localizer = momentLocalizer(moment);
  const [modal, setModal] = React.useState(false);
  const [modstartTime, modsetStartTime] = React.useState('10:00');
  const [modendTime, modsetEndTime] = React.useState('11:00');
  const [modtitle, modsetTitle] = React.useState('Title');
  const [modselectedDate, modsetSelectedDate] = useState(new Date());
  
  
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
          let event_id=event['eventid'];
          console.log(event_id);

          return {
            start,
            end,
            title,
            event_id
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
        let event_id=event['eventid'];
        console.log(event_id)
        console.log('ADDING NEW INDIVIDUAL EVENT');
        setEvents((prevEvents) => [...prevEvents, { start, end, title, event_id }]);
      });
    }, []);
  }
    const handleSubmit = (event) => {
    event.preventDefault();
    console.log(modtitle);
    console.log(modselectedDate);
    console.log(modstartTime);
    console.log(modendTime);
    const start = moment(
      modselectedDate.toISOString().split('T')[0] + ' ' + modstartTime
    ).format('X');

    const end = moment(
      modselectedDate.toISOString().split('T')[0] + ' ' + modendTime
    ).format('X');
    console.log(start);
    Socket.emit('modify event', {
      title: modtitle,
      date: modselectedDate,
      start,
      end,
      ccode: props.ccode[0],
      event_id: eventID
    });
    setModal(false);
  };

  new_Event();

  //onSelectEvent={()=> setMod({render: true }) } 
  
 // { mod.render && (<Modify ccode={props.ccode}  />)}
  return (
    <div style={{ height: '100%' }}>
      <Calendar
        //   selectable
        popup
        localizer={localizer}
        events={events}
        step={60}
        defaultView={Views.MONTHS}
        max={dates.add(dates.endOf(new Date(2015, 17, 1), 'day'), -1, 'hours')}
        scrollToTime={new Date(1970, 1, 1, 6)}
        defaultDate={new Date(2020, 10, 1)}
          onSelectEvent={ event =>{setModal(true); modsetTitle(event.title); modsetStartTime(event.start); modsetEndTime(event.end);}
           } 
        />

              <Modal
        titleAriaId={'View Event'}
        isOpen={modal}
        onDismiss={() => {
          setModal(false);
        }}
        isBlocking={false}
        // containerClassName={contentStyles.container}
        dragOptions={{
          moveMenuItemText: 'Move',
          closeMenuItemText: 'Close',
          menu: ContextualMenu
        }}
      >        <form onSubmit={handleSubmit}>
          <Stack tokens={{ childrenGap: 10, padding: 20 }}>
          <h1>{modtitle}</h1>

            <h3> Title </h3>
            <TextField
              label="title"
              value={modtitle}
              onChange={(val) => {
                modsetTitle(val.target.value);
              }}
            />

            <h3> Date </h3>
            <DatePicker value={modselectedDate} onSelectDate={modsetSelectedDate} />

            <h3> Start Time </h3>
            <Stack.Item>
              <TimePicker onChange={modsetStartTime} value={modstartTime} />
            </Stack.Item>
            <h3> End Time </h3>
            <Stack.Item>
              <TimePicker onChange={modsetEndTime} value={modendTime} />
            </Stack.Item>

            <DefaultButton onClick={handleSubmit}>Send</DefaultButton>
          </Stack>
        </form>
      </Modal>
    </div>    

  );
}
