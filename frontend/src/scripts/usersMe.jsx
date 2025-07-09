import { useState, useEffect } from "react";

export const useAuth = () => {
    const apiUrl = process.env.REACT_APP_API_URL;
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userData, setUserData] = useState('');
    const [isAuthChecked, setIsAuthChecked] = useState(false); // Добавляем состояние для проверки завершения запроса на авторизацию

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch(`${apiUrl}/users/me`, {
                    method: "GET",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                const userData = await response.json();
                setUserData(userData);
                setIsLoggedIn(true);
            } catch (error) {
                console.error("Error fetching user data:", error);
            } finally {
                setIsAuthChecked(true); // Устанавливаем состояние завершения проверки авторизации в true вне зависимости от результата запроса
            }
        };

        if (!isLoggedIn) {
            fetchUserData();
        }
    }, []);
    return { isLoggedIn, userData, isAuthChecked}; // Возвращаем также состояние isAuthChecked
};