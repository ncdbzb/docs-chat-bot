import { Link, useLocation } from 'react-router-dom';
import React, { useRef, useState } from 'react';
import './header.css';
import { logout } from '../../../scripts/logOut';
import { useAuth } from '../../../scripts/usersMe';
import siteLogo from '../../../img/icons/logo UDV group 1.png';
import arrow from '../../../img/icons/arrow_drop_down.svg';

function Header({setFlag}) {
  const location = useLocation(); // Получение текущего пути
  const { isLoggedIn, isAuthChecked, userData } = useAuth();
  const arrowClickRef = useRef(null);
  const visibilityListRef = useRef(null);
  const btnQuestionRef = useRef(null);
  const btnTestRef = useRef(null);

  const handleButtonClick = (event, isQuestion) => {
    event.preventDefault();
    if (isQuestion) {
      btnTestRef.current.classList.remove('btn-add');
      btnQuestionRef.current.classList.toggle('btn-add');
      setFlag(true);
    } else {
      btnQuestionRef.current.classList.remove('btn-add');
      btnTestRef.current.classList.toggle('btn-add');
      setFlag(false);
    }
  };

  const clickArrowLk = () => {
    if (arrowClickRef.current && visibilityListRef.current) {
      arrowClickRef.current.classList.toggle('click-arrow');
      visibilityListRef.current.classList.toggle('active');
    } else {
      console.error('Elements not found');
    }
  };

  if (!isAuthChecked) {
    return null;
  }

  return (
    <header className="page-header">
      <nav className="main-nav">
        <div className="site-navigation">
          <div className="site-navigation-item">
            <Link to="/" className="nav-udv">
              <img className="icon-logo" src={siteLogo} alt="Иконка логотипа 'UDV|Group'" />
            </Link>
          </div>
          <div className='site-navigation-item'>
            <div className="buttons">
              {location.pathname === '/request_documentation' && (
                <>
                  <button className="btn-question button button-header" onClick={(e) => handleButtonClick(e, true)} ref={btnQuestionRef}>
                    Задать вопрос
                  </button>
                  <button className="btn-test button button-header btn-add" onClick={(e) => handleButtonClick(e, false)} ref={btnTestRef}>
                    Пройти тест
                  </button>
                </>
              )}
              {isLoggedIn ? (
                <div className='container-lk'>
                  <div className="btn-user-lk" onClick={clickArrowLk}>
                    <div className='user-FIO'>
                      <p>{userData.surname}</p>
                      <p>{userData.name}</p>
                    </div>
                    <img className='btn-arrow' src={arrow} alt='' ref={arrowClickRef} />
                  </div>
                  <div className='nav-lk' ref={visibilityListRef}>
                    <Link to="/person_account" className="btn-signUp button-header">Личные данные</Link>
                    <Link to="/work_documentation" className="btn-signUp button-header">Документация</Link>
                    <Link className="btn-logOut button-header" onClick={logout}>Выйти</Link>
                  </div>
                </div>
              ) : (
                <div className='auth-container'>
                  <Link to="/logIn" className="btn-signUp button-header">Войти</Link>
                  <p> | </p>
                  <Link to="/signUp" className="btn-signIp button-header">Регистрация</Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>
    </header>
  );
}

export default Header;