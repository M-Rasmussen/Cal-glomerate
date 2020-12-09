import React, { useState } from 'react';
import { Calendar, Views, momentLocalizer } from 'react-big-calendar';
import * as dates from './dates';
import moment from 'moment';
import './CalenderStyle.css';
import { Socket } from './Socket';

import randomColor from 'randomcolor';
import TimePicker from 'react-time-picker';

import {
  ContextualMenu,
  DatePicker,
  DefaultButton,
  Modal,
  Stack,
  TextField
} from 'office-ui-fabric-react';

export function Cal_comp({ ccode, eventsToShow }) {
  console.log('skjdnf');
  console.log(eventsToShow);
  const localizer = momentLocalizer(moment);
  const [modal, setModal] = React.useState(false);
  const [modstartTime, modsetStartTime] = React.useState('11:00');
  const [modendTime, modsetEndTime] = React.useState('14:00');
  const [modtitle, modsetTitle] = React.useState('Title');
  const [modselectedDate, modsetSelectedDate] = useState(new Date());
  const [modEventId, modSetEventId] = useState(0);
  const [modEventCCode, modSetEventCCode] = useState(0);

  const handleSubmit = (event) => {
    event.preventDefault();
    const start = moment(
      modselectedDate.toISOString().split('T')[0] + ' ' + modstartTime
    ).format('X');
    const end = moment(
      modselectedDate.toISOString().split('T')[0] + ' ' + modendTime
    ).format('X');
    Socket.emit('modify event', {
      title: modtitle,
      date: modselectedDate,
      start,
      end,
      ccode: modEventCCode,
      event_id: modEventId,
      ccode_list: ccode
    });
    setModal(false);
  };
  function modEventTime(event) {
    let unformattedStart = new Date(event.start).toLocaleTimeString('en-US', {
      hour12: false
    });
    let formattedStart = unformattedStart.slice(0, 5);
    modsetStartTime(formattedStart);

    let unformattedEnd = new Date(event.end).toLocaleTimeString('en-US', {
      hour12: false
    });
    let formattedEnd = unformattedEnd.slice(0, 5);
    modsetEndTime(formattedEnd);
  }
  const handleDelete = (event) => {
    event.preventDefault();

    Socket.emit('delete event', {
      ccode: modEventCCode,
      event_id: modEventId,
      ccode_list: ccode
    });
    setModal(false);
  };
  return (
    <div style={{ height: '100%' }}>
      <Calendar
        //   selectable
        localizer={localizer}
        events={eventsToShow}
        step={60}
        defaultView={Views.MONTHS}
        max={dates.add(dates.endOf(new Date(2015, 17, 1), 'day'), -1, 'hours')}
        scrollToTime={new Date(1970, 1, 1, 6)}
        defaultDate={new Date(2020, 10, 1)}
        onSelectEvent={(event) => {
          setModal(true);
          modsetTitle(event.title);
          modsetSelectedDate(event.start);
          modEventTime(event);
          modSetEventId(event.event_id);
          modSetEventCCode(event.ccode[0]);
        }}
        eventPropGetter={(event, start, end, isSelected) => {
          const backgroundColor = randomColor({ seed: event.ccode[0] * 1000 });
          const style = {
            backgroundColor: backgroundColor,
            // borderRadius: '0px',
            opacity: 0.8,
            color: 'black',
            border: '0px',
            display: 'block'
          };
          return { style };
        }}
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
      >
        {' '}
        <form onSubmit={handleSubmit}>
          <Stack tokens={{ childrenGap: 10, padding: 20 }}>
            <h1>{modtitle}</h1>
            <h3>{modEventCCode}</h3>
            <TextField
              label="title"
              value={modtitle}
              onChange={(val) => {
                modsetTitle(val.target.value);
              }}
            />

            <h3> Date </h3>
            <DatePicker
              value={modselectedDate}
              onSelectDate={modsetSelectedDate}
            />

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
        <DefaultButton onClick={handleDelete}>Delete </DefaultButton>
      </Modal>
    </div>
  );
}
