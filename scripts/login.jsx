import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import { GoogleLogin } from 'react-google-login';
import { Socket } from './Socket';
import './loginstyle.css';
import { Cal_comp } from './CalenderComp.jsx';
import { HomePage } from './LogedInHome';
import { Image, ImageFit, Stack } from 'office-ui-fabric-react';

export default function Login() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [ccode, setCcode] = useState([-1]);
  const [userId, setUserId] = useState('');
  const [token, setToken] = useState('');

  function loginUser(response) {
    Socket.emit('new google user', {
      code: response['code']
    });
  }

  function loginUserFail() {
    return false;
  }

  function verifiedSession() {
    React.useEffect(() => {
      Socket.on('Verified', (data) => {
        setLoggedIn(true);
        setUsername(data.name);
        setCcode(data.ccodes);
        setUserId(data.userid);
        setToken(data.access_token);
      });
    }, []);
  }

  verifiedSession();

  if (loggedIn && ccode[0] != -1) {
    return (
      <div
        className="outermost"
        style={{ backgroundColor: 'azure', height: '100%' }}
      >
        <Stack
          horizontal
          horizontalAlign="center"
          verticalAlign="center"
          style={{ color: 'blue' }}
        >
          <Image
            src="/static/logo.png"
            imageFit={ImageFit.contain}
            width={100}
            height={100}
          />
          <h1 style={{ textShadow: '0 0 3px #FFFFFF, 0 0 5px #0000FF' }}>
            Calglomerate
          </h1>
        </Stack>
        <div className="header"></div>
        <div className="container">
          <HomePage ccode={ccode} userId={userId} access_token={token} />
        </div>
      </div>
    );
  }
  return (
    <Stack
      verticalAlign="start"
      horizontalAlign="center"
      tokens={{ childrenGap: 10, padding: 20 }}
      style={{ backgroundColor: 'azure', height: '100%' }}
    >
      <Stack
        horizontal
        horizontalAlign="center"
        verticalAlign="center"
        style={{ color: 'blue' }}
      >
        <Image
          src="/static/logo.png"
          imageFit={ImageFit.contain}
          width={100}
          height={100}
        />
        <h1 style={{ textShadow: '0 0 3px #FFFFFF, 0 0 5px #0000FF' }}>
          Calglomerate
        </h1>
      </Stack>

      <div className="header" style={{ width: '100vw' }}></div>
      <Stack tokens={{ childrenGap: 10, padding: 20 }}>
        <Stack.Item>
          <Stack
            horizontal
            horizontalAlign="center"
            verticalAlign="center"
            style={{
              border: '5px solid blue',
              borderRadius: '2%',
              backgroundColor: 'lightblue'
            }}
          >
            <h2>
              Have you ever wanted to find a time to meet with your friends?
            </h2>
            <Image
              src="/static/friends.png"
              imageFit={ImageFit.contain}
              width={125}
              height={125}
            />
          </Stack>
        </Stack.Item>

        <Stack.Item>
          <Stack
            horizontal
            horizontalAlign="center"
            verticalAlign="center"
            style={{
              border: '5px solid blue',
              borderRadius: '2%',
              backgroundColor: 'lightblue'
            }}
          >
            <Image
              src="/static/organized.png"
              imageFit={ImageFit.contain}
              width={125}
              height={125}
            />
            <h3>
              Does having multiple accounts with calendars ever make it
              difficult to stay organized?
            </h3>
          </Stack>
        </Stack.Item>

        <Stack.Item>
          <Stack
            horizontal
            horizontalAlign="center"
            verticalAlign="center"
            style={{}}
          >
            {/* <Image
              src="/static/logo.png"
              imageFit={ImageFit.contain}
              width={150}
              height={150}
            /> */}
            <h1
              style={{
                color: 'blue',
                // border: '5px solid blue',
                // borderRadius: '2%',
                // backgroundColor: 'lightblue',
                // padding: '20px',
                fontSize: '4em',
                textShadow: '0 0 3px #FFFFFF, 0 0 5px #0000FF'
              }}
            >
              Calglomerate is here to help!
            </h1>
          </Stack>
        </Stack.Item>

        <Stack
          horizontal
          horizontalAlign="center"
          verticalAlign="center"
          tokens={{ childrenGap: 10 }}
        >
          <Stack
            horizontal
            horizontalAlign="center"
            verticalAlign="center"
            tokens={{ childrenGap: 10, padding: 20 }}
            style={{
              border: '5px solid blue',
              borderRadius: '2%',
              backgroundColor: 'lightblue'
            }}
          >
            <h1>Have an account? Login here:</h1>
            <div>
              <GoogleLogin
                clientId="658056760445-ejq8q635n1948vqieqf95vsa6c6e1fvp.apps.googleusercontent.com"
                scope="https://www.googleapis.com/auth/calendar.readonly"
                buttonText="Login"
                onSuccess={loginUser}
                onFailure={loginUserFail}
                accessType="offline"
                responseType="code"
                cookiePolicy="single_host_origin"
              />
            </div>
          </Stack>
        </Stack>

        <Stack
          horizontal
          horizontalAlign="center"
          verticalAlign="center"
          tokens={{ childrenGap: 10, padding: 20 }}
        >
          <Stack
            horizontal
            horizontalAlign="center"
            verticalAlign="center"
            tokens={{ childrenGap: 10, padding: 20 }}
            style={{
              border: '5px solid blue',
              borderRadius: '2%',
              backgroundColor: 'lightblue'
            }}
          >
            <h1>Get started now!</h1>
            <div>
              <GoogleLogin
                clientId="658056760445-ejq8q635n1948vqieqf95vsa6c6e1fvp.apps.googleusercontent.com"
                scope="https://www.googleapis.com/auth/calendar.readonly"
                buttonText="Register"
                onSuccess={loginUser}
                onFailure={loginUserFail}
                accessType="offline"
                responseType="code"
                cookiePolicy="single_host_origin"
              />
            </div>
          </Stack>
        </Stack>
      </Stack>
    </Stack>
  );
}
