import * as React from 'react';
import { Cal_comp } from './CalenderComp';
import { Create_event } from './Add_Event';
import { MergeCalenders } from './MergeCalComp';
import { Create_cal } from './Add_Cal';
import './HomePage.css';
import { Stack } from 'office-ui-fabric-react';
import { Card } from '@uifabric/react-cards';
import { Socket } from './Socket';
import { CalendarSelector } from './CalendarSelector';

export function HomePage({ ccode, userId }) {
  const [events, setEvents] = React.useState([]);
  const [eventsToShow, setEventsToShow] = React.useState([]);

  React.useEffect(() => {
    Socket.emit('get events', ccode[0]);
    Socket.on('recieve all events', (data) => {
      console.log(data);
      setEvents(
        data.map((event) => {
          let intstart = parseInt(event['start']);
          let start = new Date(intstart * 1000);
          let intend = parseInt(event['end']);
          let end = new Date(intend * 1000);
          let title = event['title'];
          let event_id = event['eventid'];
          console.log(event_id);

          const ccode = event['ccode'];
          return {
            start,
            end,
            title,
            event_id,
            ccode
          };
        })
      );
      setEventsToShow(events);
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
        let event_id = data['eventid'];
        let ccode = data['ccode'];
        console.log(event_id);
        console.log('ADDING NEW INDIVIDUAL EVENT');
        setEvents((prevEvents) => [
          ...prevEvents,
          { start, end, title, event_id, ccode }
        ]);
        setEventsToShow(events);
      });
    }, []);
  }
  new_Event();

  return (
    <div className="conent_wrapper">
      <div className="interact_side">
        <Stack tokens={{ childrenGap: 20, padding: 5 }}>
          <MergeCalenders ccode={ccode} />
          <Create_event ccode={ccode} />
          <Create_cal userId={userId} />
          <CalendarSelector
            events={events}
            eventsToShow={eventsToShow}
            setEventsToShow={setEventsToShow}
          />
        </Stack>
      </div>
      <div className="calender_side">
        <Card style={{ maxWidth: 'none', padding: '5px', background: 'white' }}>
          <Cal_comp ccode={ccode} events={eventsToShow} />
        </Card>
      </div>
    </div>
  );
}
