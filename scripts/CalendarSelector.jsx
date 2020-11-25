import { Card } from '@uifabric/react-cards';
import {
  Checkbox,
  DefaultButton,
  Stack,
  TextField
} from 'office-ui-fabric-react';
import React, { useState } from 'react';

export function CalendarSelector({ events, eventsToShow, setEventsToShow }) {
  const ccodes = [...new Set(events.map((event) => event.ccode[0]))];

  const [showCcode, setShowCcode] = useState(
    ccodes.map((ccode) => {
      return { ccode, show: true };
    })
    // ccodes.reduce((acc, ccode) => {
    //   console.log(acc);
    //   acc[ccode] = true;
    // }, {})
  );

  console.log(showCcode);
  console.log(
    ccodes.map((ccode) => {
      return { ccode, show: true };
    })
  );

  const toggleCcode = (ccode) => {
    const newShowCcode = showCcode;
    newShowCcode[ccode] = !newShowCcode[ccode];
    setShowCcode(newShowCcode);
    setEventsToShow(events.filter((event) => showCcode[event.ccode[0]]));
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
                    <Checkbox
                      label={`ccode: ${ccode}`}
                      checked={showCcode[ccode]}
                      onChange={() => {
                        toggleCcode(ccode);
                      }}
                    />
                  );
                })}
              </Stack.Item>
            </Stack>
          </Card.Item>
        </Card>
      </Stack>
    </div>
  );
}
