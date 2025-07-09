import { useState } from "react";

export const useRequestEditDocumentation = () => {
    const apiUrl = process.env.REACT_APP_API_URL;
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const sendRequest = async ({ currentName, newName, description, setFlag, setMessage }) => {
        try {
            const data = {
              current_name: currentName,
              new_name: newName,
              description: description,
            };

            const response = await fetch(`${apiUrl}/docks/change_data`, {
                method: 'PATCH',
                credentials: 'include',
                body: JSON.stringify(data),
                headers: {
                  'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            setMessage('Данные успешно изменены!');
            setFlag(true);
            setIsLoggedIn(true);
            return response.json();
        } catch (error) {
            console.error('Error fetching user data:', error);
            throw error;
        }
    };

    return { sendRequest, isLoggedIn };
};