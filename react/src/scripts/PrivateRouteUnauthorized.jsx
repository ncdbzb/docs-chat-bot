import React from 'react';
import { Route, Navigate, Outlet} from 'react-router-dom';
import { useAuth } from './usersMe';

export const PrivateRouteUnauthorized = () => {
  // Проверяем аутентификацию пользователя
  
    const { isLoggedIn, isAuthChecked } = useAuth();
    if (!isAuthChecked) {
        // Если проверка авторизации еще не завершена, ничего не отображаем
        return null;
    }
    return(
        isLoggedIn? <Outlet /> : <Navigate to="/logIn" />
    );
}
