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

export function Import_cal({ userId, ccode, access_token }) {
  const [modal, setModal] = useState(false);
  const [title, setTitle] = useState('Title');
  const [priv, setPriv] = useState(false);
  const currUser = userId;
  const accessToken = access_token;
  
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(title);
    console.log(priv);
    Socket.emit('Import Calendar', {
      title: title,
      userid: currUser,
      privateCal: priv,
      ccode_list: ccode,
      accessToken: accessToken
    });
    console.log("Emitted!");
    setModal(false);
    setPriv(false);
  };

  return (
    <div>
      <Card style={{ background: 'white' }}>
        <DefaultButton
          text="Import Calendar"
          onClick={() => {
            setModal(true);
          }}
          allowDisabledFocus
        />
      </Card>
      <Modal
        titleAriaId={'Import Calendar'}
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
            <h1>Import Calendar</h1>
            <label for="private"> Make Calendar Private</label>
            <input type="checkbox" id="private" onChange={() => {setPriv(!priv)}} defaultChecked={priv}/>
            <DefaultButton onClick={handleSubmit}>Send</DefaultButton>
          </Stack>
        </form>
      </Modal>
    </div>
  );
}
