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
  IIconProps
} from 'office-ui-fabric-react';
import React, { useEffect, useState } from 'react';
import './HomePage.css';

export function CalendarSelector({ events, setEventsToShow, userId }) {
  const [modal, setModal] = useState(false);
  const [calTitle, setcalTitle] = useState(0);
  const [deleteCal, setDeleteCal] = useState(false);
  const [ccodeDetails, setCcodeDetails] = useState({});

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

    Socket.emit('get ccode details', ccodes);
    Socket.on('recieve ccode details', (newCcodeDetails) => {
      console.log(newCcodeDetails);
      setCcodeDetails(newCcodeDetails);
      setDeleteCal(false);
    });
  }, [events]);

  const toggleCcode = (ccode) => {
    const newShowCcode = showCcode;
    newShowCcode[ccode] = !newShowCcode[ccode];
    setShowCcode(newShowCcode);
    setEventsToShow(events.filter((event) => showCcode[event.ccode[0]]));
  };

  const emojiIcon = { iconName: 'Settings' };

  const toggleCcodePrivacy = (ccode) => {
    const newCcodeDetails = ccodeDetails;
    newCcodeDetails[ccode] = !newCcodeDetails[ccode];
    setCcodeDetails(newCcodeDetails);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(calTitle);
    console.log('Current user:' + currUser);
    console.log(ccodeDetails);
    const isPrivate =
      (ccodeDetails[calTitle].hasOwnProperty('privateCal') &&
        ccodeDetails[calTitle].privateCal) ||
      ccodeDetails[calTitle];
    const data = {
      ccode: calTitle,
      userid: currUser,
      privateCal: isPrivate,
      deleteCal: deleteCal,
      allCcodes: ccodes
    };
    console.log(data);
    Socket.emit('modify calendar', data);
    console.log('Emitted!');
    setModal(false);
  };

  const getCcodePrivacy = (ccode) => {
    if (!(ccode in ccodeDetails)) {
      return 'Unknown!';
    } else if (ccodeDetails[ccode].private) {
      return 'Private';
    } else {
      return 'Public';
    }
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
                        className="floatLeft"
                        label={`ccode: ${ccode} ${getCcodePrivacy(ccode)}`}
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
                        }}
                      />
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
            <h3> ccode:{calTitle} </h3>

            <Checkbox
              label="Toggle to change calendar privacy"
              onChange={() => {
                toggleCcodePrivacy(calTitle);
              }}
            />
            <Checkbox
              label="Toggle to Delete Calendar"
              onChange={() => {
                setDeleteCal(!deleteCal);
              }}
            />
            <DefaultButton onClick={handleSubmit}>
              Confirm changes
            </DefaultButton>
          </Stack>
        </form>
      </Modal>
    </div>
  );
}
