import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Main from './sitePagesRouting/main';
import SignUp from './sitePagesRouting/signUp';
import LogIn from './sitePagesRouting/logIn';
import Request from './sitePagesRouting/requestDocumentation'
import UploadFile from './sitePagesRouting/uploadFile';
import PersonArea from './sitePagesRouting/personArea';
import {PrivateRouteUnauthorized} from './scripts/PrivateRouteUnauthorized';
import { PrivateRouteAuthorized } from './scripts/PrivateRouteAuthorized';
import FormForgotPassword from './sitePagesRouting/forgotPassword';
import FormResetPassword from './sitePagesRouting/resetPassword';
import LeaderboardDatapkPage from './sitePagesRouting/leaderboardDatapk';
import Work from './sitePagesRouting/Work';


function App() {  
  return (
      <BrowserRouter>
        <Routes>
            <Route path="/" element={<Main /> } />
            {/* Измененный маршрут */}
            <Route path="/request_documentation" element={<Request />} />
            <Route path="/work_documentation" element={<Work  />} />
            <Route path="/forgot_password" element={<FormForgotPassword/>} />
            <Route path="/reset_password" element={<FormResetPassword/>} />
            <Route element={<PrivateRouteUnauthorized />} >
              <Route path="/upload_file" element={<UploadFile />} />
              <Route path="/person_account" element={<PersonArea />} />
            </Route>
            <Route element={<PrivateRouteAuthorized />}>
              <Route path="/signUp" element={<SignUp />} />
              <Route path="/logIn" element={<LogIn />} />
            </Route>
            <Route path='/leaderboard/DATAPK_VERSION_2_1'  element={<LeaderboardDatapkPage data='DATAPK_VERSION_2_1'  />} />
            <Route path='/leaderboard/DATAPK_ITM_VERSION_1_7'  element={<LeaderboardDatapkPage data='DATAPK_ITM_VERSION_1_7'  />} />
        </Routes>
      </BrowserRouter>
  )
}

export default App;
