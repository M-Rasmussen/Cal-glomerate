import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import { GoogleLogin } from 'react-google-login';
import { Socket } from './Socket';
import './loginstyle.css';
import { Cal_comp } from './CalenderComp.jsx';
import { HomePage } from './LogedInHome';

export default function Login() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [ccode, setCcode] = useState([-1]);
  const [userId, setUserId] = useState('');
  const [token, setToken] = useState('');

  function loginUser(response) {
    const name = response.getBasicProfile().getName();
    const email = response.getBasicProfile().getEmail();
    const idToken = response.getAuthResponse().id_token;
    const access_token = response.getAuthResponse().access_token;
    console.log("AUTH TOKEN IS:" + access_token);
    Socket.emit('new google user', {
      name: name,
      email: email,
      idtoken: idToken,
      access_token: access_token
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
      <div className="outermost">
        <h1 className="header">Calglomerate</h1>
        <div className="container">
          <HomePage ccode={ccode} userId={userId} access_token={token} />
        </div>
      </div>
    );
  }
  return (
    <div className="outermost">
      <h1 className="header">Calglomerate</h1>
      <div className="container">
        <GoogleLogin
          clientId="658056760445-ejq8q635n1948vqieqf95vsa6c6e1fvp.apps.googleusercontent.com"
          scope="https://www.googleapis.com/auth/calendar.readonly"
          buttonText="Login"
          onSuccess={loginUser}
          onFailure={loginUserFail}
          cookiePolicy="single_host_origin"
        />
      </div>
    </div>
  );
}
