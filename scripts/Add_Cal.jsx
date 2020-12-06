import React, { useState } from 'react';
import { Socket } from './Socket';
import {
  ContextualMenu,
  DefaultButton,
  Modal,
  Stack,
  TextField
} from 'office-ui-fabric-react';
import { Card } from '@uifabric/react-cards';

export function Create_cal({ userId, ccode }) {
  const [modal, setModal] = useState(false);
  const [title, setTitle] = useState('Title');
  const [priv, setPriv] = useState(false);
  const currUser = userId;
  
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(title);
    console.log(priv);
    console.log("Current user:" + currUser);
    Socket.emit('add calendar', {
      title: title,
      userid: currUser,
      privateCal: priv,
      ccode_list: ccode
    });
    console.log("Emitted!");
    setModal(false);
    setPriv(false);
  };

  return (
    <div>
      <Card style={{ background: 'white' }}>
        <DefaultButton
          text="Add Calendar"
          onClick={() => {
            setModal(true);
          }}
          allowDisabledFocus
        />
      </Card>
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
            <h1>Add Calendar</h1>

            <h3> Title </h3>
            <TextField
              label="title"
              value={title}
              onChange={(val) => {
                setTitle(val.target.value);
              }}
            />
            <label for="private"> Make Calendar Private</label>
            <input type="checkbox" id="private" onChange={() => {setPriv(!priv)}} defaultChecked={priv}/>
            <DefaultButton onClick={handleSubmit}>Send</DefaultButton>
          </Stack>
        </form>
      </Modal>
    </div>
  );
}
