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
  const localizer = momentLocalizer(moment);
  const [modal, setModal] = React.useState(false);
  const [modstartTime, modsetStartTime] = React.useState(new Date());
  const [modendTime, modsetEndTime] = React.useState(new Date());
  const [modtitle, modsetTitle] = React.useState('Title');
  const [modselectedDate, modsetSelectedDate] = useState(new Date());
  const [modEventId, modSetEventId] = useState(0);

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(modtitle);
    console.log(modselectedDate);
    console.log(modstartTime);
    console.log(modendTime);
    console.log(modEventId);
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
      ccode: ccode[0],
      event_id: modEventId
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
          modsetStartTime(event.start);
          modsetEndTime(event.end);
          modSetEventId(event.event_id);
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
      </Modal>
    </div>
  );
}
