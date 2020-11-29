import { Card } from '@uifabric/react-cards';
import { Socket } from './Socket';
import {
  ContextualMenu,
  Modal,
  Checkbox,
  DefaultButton,
  Stack,
  TextField,
  IconButton,
  IIconProps,
} from 'office-ui-fabric-react';
import React, { useEffect, useState } from 'react';
import './HomePage.css';


export function CalendarSelector({ events, setEventsToShow, userId }) {
  const [modal, setModal] = useState(false);
  const [calTitle, setcalTitle] = useState(0);
  const [priv, setPriv] = useState(false);
  const [deleteCal, setDeleteCal] = useState(false);
  const currUser = userId;
  //NEED TO GET CURRENT USER ID PROPS USER ID TODO
  
  
  const ccodes = [...new Set(events.map((event) => event.ccode[0]))];

  const [showCcode, setShowCcode] = useState({});
  useEffect(() => {
    const initialshowCcode = Object.fromEntries(
      ccodes.map((ccode) => [ccode, true])
    );
    console.log(initialshowCcode);
    setShowCcode(initialshowCcode);
    setEventsToShow(events.filter((event) => initialshowCcode[event.ccode[0]]));
  }, [events]);

  const toggleCcode = (ccode) => {
    const newShowCcode = showCcode;
    newShowCcode[ccode] = !newShowCcode[ccode];
    setShowCcode(newShowCcode);
    setEventsToShow(events.filter((event) => showCcode[event.ccode[0]]));
    //filter out event. 
  };

 const emojiIcon = { iconName: 'Settings' };


  
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(calTitle);
    console.log(priv);
    console.log("Current user:" + currUser);
    Socket.emit('modify calendar', {
      ccode: calTitle,
      userid: currUser,
      privateCal: priv,
      deleteCal: deleteCal
    });
    console.log("Emitted!");
    setModal(false);
  };
  return (
    <div>
      <Stack tokens={{ childrenGap: 10 }}>
        <Card style={{ background: 'white' }}>
          <Card.Item>
            <h3 style={{ paddingTop: '20px' }}>Calendars to View</h3>
          </Card.Item>
          <Card.Item>
            <Stack horizontal tokens={{ childrenGap: 0, padding: 5 }}>
              <Stack.Item grow={1}>
                {ccodes.map((ccode) => {
                  return (
                    <div>
                    <Checkbox
                      className= "floatLeft"
                      label={`ccode: ${ccode}`}
                      checked={showCcode[ccode]}
                      onChange={() => {
                        toggleCcode(ccode);
                      }}
                    />
                    <IconButton 
                      style={{ width: '20%' }} 
                      iconProps={emojiIcon} 
                      title="Settings" 
                      ariaLabel="Settings" 
                      onClick={() => {
                        setcalTitle(ccode);
                        setModal(true);
                        
                      }} />
                    </div>
                  );
                })}
              </Stack.Item>
            </Stack>
          </Card.Item>
        </Card>
      </Stack>
      <Modal
        titleAriaId={'Add Calendar'}
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
            
            <h3> ccode:{ calTitle } </h3>
           
            <Checkbox
            label='Toggle to change calendar privacy'
            onChange={() => {
                        setPriv(!priv);
            }}
                    />
            <Checkbox
            label='Toggle to Delete Calendar'
            onChange={() => {
                        setDeleteCal(!priv);
            }}
                    />
            <DefaultButton onClick={handleSubmit}>Confirm changes</DefaultButton>
          </Stack>
        </form>
      </Modal>
    </div>
  );
}
