import React, { useState } from 'react';
import { GoogleLogin } from 'react-google-login';
import {
  ContextualMenu,
  DefaultButton,
  Image,
  ImageFit,
  Modal,
  Stack,
} from 'office-ui-fabric-react';
import { HomePage } from './LogedInHome';
import { Socket } from './Socket';
import './loginstyle.css';

export default function Login() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [ccode, setCcode] = useState([-1]);
  const [userId, setUserId] = useState('');
  const [token, setToken] = useState('');
  const [modal, setModal] = useState(false);

  function loginUser(response) {
    Socket.emit('new google user', {
      code: response.code,
    });
  }

  function loginUserFail() {
    return false;
  }

  function verifiedSession() {
    React.useEffect(() => {
      Socket.on('Verified', (data) => {
        setLoggedIn(true);
        setCcode(data.ccodes);
        setUserId(data.userid);
        setToken(data.access_token);
      });
    }, []);
  }

  verifiedSession();

  if (loggedIn && ccode[0] !== -1) {
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
        <div className="header" />
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

      <div className="header" style={{ width: '100vw' }} />
      <Stack tokens={{ childrenGap: 10, padding: 20 }}>
        <Stack.Item>
          <Stack
            horizontal
            horizontalAlign="center"
            verticalAlign="center"
            style={{
              border: '5px solid blue',
              borderRadius: '2%',
              backgroundColor: 'lightblue',
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
              backgroundColor: 'lightblue',
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
                textShadow: '0 0 3px #FFFFFF, 0 0 5px #0000FF',
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
              backgroundColor: 'lightblue',
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
              backgroundColor: 'lightblue',
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
        <Stack horizontal horizontalAlign="center" verticalAlign="center">
          <DefaultButton
            style={{
              border: '5px solid blue',
              borderRadius: '2%',
              backgroundColor: 'lightblue',
            }}
            iconProps={{ iconName: 'Info' }}
            title="Settings"
            ariaLabel="Settings"
            onClick={() => {
              setModal(true);
            }}
          >
            About Calglomerate
          </DefaultButton>
        </Stack>
        <Modal
          titleAriaId="About Calglomerate"
          isOpen={modal}
          onDismiss={() => {
            setModal(false);
          }}
          isBlocking={false}
          dragOptions={{
            moveMenuItemText: 'Move',
            closeMenuItemText: 'Close',
            menu: ContextualMenu,
          }}
        >
          <div style={{ padding: '10px' }}>
            <h2>About Calglomerate</h2>
            <ul>
              <li>Who are We?</li>
              <ul>
                <li>
                  We’re a team of four Computer Science college students from
                  NJIT - Samuel Carlos, David Balcon, Mathew Rasmussen, and
                  Harsh Patel - who sought to solve an issue with time. For many
                  of us, time is a scarce resource and time after time we’re
                  told to take advantage of it, yet, for many of us organizing
                  it is a tall task, and even more so when you add your friends
                  into the picture.
                </li>
              </ul>
              <li>What is Calglomerate?</li>
              <ul>
                <li>
                  Therefore, we’ve made Calglomerate - an application to make
                  meeting management easier. With Calglomerate, you can easily
                  create events. Managing multiple calendars is also a breeze
                  with our calendar merging algorithms - So you can keep your
                  work calendar separate from your personal calendar while
                  remaining organized. Best of all, it’s as simple as a click to
                  share them with your friends! Just input a code they send you
                  and boom - you’re instantly subscribed to them.
                </li>
              </ul>
              <li>How does it work?</li>
              <ul>
                <li>
                  For the backend, we used python, flask, sqlalchemy for the
                  database. For the frontend, we used React, OAuth Api, google
                  calendar Api. SocketIO was used to link the frontend and
                  backend together.
                </li>
              </ul>
              <li>Why we&apos;ve made it?</li>
              <ul>
                <li>
                  Many people have multiple Calendars and Have you ever had an
                  issue with trying to plan out your events with others? Trying
                  to figure out when you are free or if you have conflicting
                  events on your multiple calendars, Calglomerate is there for
                  you. We give users the ability to merge their calendars with
                  others.
                </li>
              </ul>
              <li>Where can you see Calglomerate?</li>
              <ul>
                <li>
                  <a href="http://calglomerate.herokuapp.com/ ">
                    calglomerate.herokuapp.com/
                  </a>
                  - You’re already here!
                </li>
              </ul>
            </ul>
          </div>
        </Modal>
      </Stack>
    </Stack>
  );
}
