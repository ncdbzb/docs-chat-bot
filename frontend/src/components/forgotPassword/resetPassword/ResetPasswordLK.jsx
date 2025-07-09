const apiUrl = process.env.REACT_APP_API_URL;

export const ResetPasswordLK = async ({data, setMessage, setFlag}) => {

    try {
        const response = await fetch(`${apiUrl}/users/me`, {
            method: "PATCH",
            credentials: "include",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const errorData = await response.json();
            if (response.status === 400) {
                if (errorData.detail === 'UPDATE_USER_EMAIL_ALREADY_EXISTS') {
                    return { error: 'Данный email уже зарегистрирован' };
                }
                if (errorData.detail.code === 'UPDATE_USER_INVALID_PASSWORD') {
                    return { error: 'Введён неверный пароль' };
                }
            }
            throw new Error("Network response was not ok");
        }
        setMessage('Данные успешно изменены')
        setFlag(true)
    } catch (error) {
        console.error("Error fetching user data:", error);
        return { error: error.message };
    }
    return null;
};