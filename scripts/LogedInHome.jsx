import * as React from 'react';
import { Cal_comp } from './CalenderComp';
import { Create_event } from './Add_Event';
import { MergeCalenders } from './MergeCalComp';
import { Create_cal } from './Add_Cal';
import './HomePage.css';
import { Stack } from 'office-ui-fabric-react';
import { Card } from '@uifabric/react-cards';
export function HomePage({ ccode, userId }) {
  return (
    <div className="conent_wrapper">
      <div className="interact_side">
        <Stack tokens={{ childrenGap: 20, padding: 5 }}>
          <MergeCalenders ccode={ccode} />
          <Create_event ccode={ccode} />
          <Create_cal userId={userId} />
        </Stack>
      </div>
      <div className="calender_side">
        <Card style={{ maxWidth: 'none', padding: '5px', background: 'white' }}>
          <Cal_comp ccode={ccode}/>
        </Card>
      </div>
    </div>
  );
}
