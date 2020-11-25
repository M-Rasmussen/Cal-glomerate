import { Card } from '@uifabric/react-cards';
import {
  Checkbox,
  DefaultButton,
  Stack,
  TextField
} from 'office-ui-fabric-react';
import React, { useEffect, useState } from 'react';

export function CalendarSelector({ events, setEventsToShow }) {
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
