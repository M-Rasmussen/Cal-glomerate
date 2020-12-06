import React, { useState } from 'react';
import moment from 'moment';
import { Socket } from './Socket';
import TimePicker from 'react-time-picker';
import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';
import {
  ContextualMenu,
  DatePicker,
  DefaultButton,
  Modal,
  Stack,
  TextField
} from 'office-ui-fabric-react';
import { Card } from '@uifabric/react-cards';

export function Create_event(props) {
  const [modal, setModal] = React.useState(false);
  const [startTime, setStartTime] = React.useState('10:00');
  const [endTime, setEndTime] = React.useState('11:00');
  const [title, setTitle] = React.useState('Title');
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [pickedCode, setpickedCode] = useState(0);
  //   const now = moment().hour(0).minute(0);
  //   const format = 'hh:mm a';
  //   React.useEffect(() => {
  //     Socket.emit('get events', props.ccode[0]);
  //   }, []);
  const cal_options = props.ccode;
  console.log("here are options: " , cal_options)
  console.log(typeof(cal_options))
  const defaultOption = cal_options[0];
  console.log(typeof(defaultOption))
  console.log("Current" ,pickedCode)
  
  
  Socket.on('update dropdown', (data) => {
      
      let newCal = data['ccode']; 
      var n = cal_options.includes(newCal)
      console.log(typeof(newCal))
      console.log(typeof(n))
      if (!n){
        cal_options.push(newCal)
      }
      
    });
 
  const handleSubmit = (event) => {
    
    event.preventDefault();
    
    console.log(title);
    console.log(selectedDate);
    console.log(startTime);
    console.log(endTime);
    const start = moment(
      selectedDate.toISOString().split('T')[0] + ' ' + startTime
    ).format('X');

    const end = moment(
      selectedDate.toISOString().split('T')[0] + ' ' + endTime
    ).format('X');
    console.log(start);
    console.log(props.ccode);
    Socket.emit('new event', {
      title: title,
      date: selectedDate,
      start,
      end,
      ccode: pickedCode['value']
    });
    setModal(false);
  };

  return (
    <div>
      <Card style={{ background: 'white' }}>
        <DefaultButton
          text="Add Event"
          onClick={() => {
            setModal(true);
          }}
          allowDisabledFocus
        />
      </Card>
      <Modal
        titleAriaId={'Add Event'}
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
        <form onSubmit={handleSubmit}>
          <Stack tokens={{ childrenGap: 10, padding: 20 }}>
            <h1>Add Event</h1>
            <h3>Select Calendar </h3>
            <Dropdown options={cal_options} value={defaultOption} onChange={(val) => {
                setpickedCode(val);
              }}  placeholder="Select ccode"/>
            <h3> Title </h3>
            <TextField
              label="title"
              value={title}
              onChange={(val) => {
                setTitle(val.target.value);
              }}
            />

            <h3> Date </h3>
            <DatePicker value={selectedDate} onSelectDate={setSelectedDate} />

            <h3> Start Time </h3>
            <Stack.Item>
              <TimePicker onChange={setStartTime} value={startTime} />
            </Stack.Item>
            <h3> End Time </h3>
            <Stack.Item>
              <TimePicker onChange={setEndTime} value={endTime} />
            </Stack.Item>

            <DefaultButton onClick={handleSubmit}>Send</DefaultButton>
          </Stack>
        </form>
      </Modal>
    </div>
  );
}
