import { Card } from '@uifabric/react-cards';
import { DefaultButton, Stack, TextField } from 'office-ui-fabric-react';
import React, { useState } from 'react';
import { Socket } from './Socket';

export function MergeCalenders({ ccode }) {
  const [mergeInput, setMergeInput] = useState('');
  function handleSubmit(event) {
    event.preventDefault();
    Socket.emit('cCodeToMerge', {
      currentUser: ccode[0],
      userToMergeWith: mergeInput,
      ccode_list: ccode
    });
    console.log(
      `you entered the C-code ${mergeInput} your calender will merge with that input`
    );
    setMergeInput('');
  }

  function changed(event) {
    console.log(mergeInput);
    setMergeInput(event.target.value);
  }

  return (
    <div>
      <Stack tokens={{ childrenGap: 10 }}>
        <Card style={{ background: 'white' }}>
          <h2>Actions</h2>
        </Card>

        <Card style={{ background: 'white' }}>
          <p>Your Calender code is {ccode[0]}</p>
        </Card>
        <Card style={{ background: 'white' }}>
          <Card.Item>
            <h3 style={{ paddingTop: '20px' }}>Add someone else's calendar</h3>
          </Card.Item>
          <Card.Item>
            <form onSubmit={handleSubmit}>
              <Stack horizontal tokens={{ childrenGap: 0, padding: 5 }}>
                <Stack.Item grow={4}>
                  <TextField
                    type="text"
                    value={mergeInput}
                    onChange={changed}
                    placeholder="########"
                  />
                </Stack.Item>
                <Stack.Item grow={1}>
                  <DefaultButton onClick={handleSubmit}>
                    Merge Calendars
                  </DefaultButton>
                </Stack.Item>
              </Stack>
            </form>
          </Card.Item>
        </Card>
      </Stack>
    </div>
  );
}
