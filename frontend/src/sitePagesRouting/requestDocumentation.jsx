import React, { useState, useEffect  } from 'react';
import FormRequestAnswQuest from '../components/requestAnswerQuestion/formRequestAnswer/FormRequestAnswQuest';
import FormRequestsTest from '../components/requestTest/FormRequstTest';
import Header from '../components/main/header/Header';
const Request = ( ) => {
  const [flag, setFlag] = useState(false);
  const params = new URLSearchParams(window.location.search);
  const docName = params.get('documentation');
  useEffect(() => {
    return () => {
      localStorage.removeItem('storageTest'); // Удаление конкретного элемента из localStorage idRequest
      localStorage.removeItem('rightAnswer'); 
      localStorage.removeItem('idRequest');
    };
  }, []);
  return (
    <>
      <Header setFlag={setFlag}/>
      {flag ? <FormRequestAnswQuest docName={docName} /> : <FormRequestsTest docName={docName} />}
    </>
  );
};

export default Request;