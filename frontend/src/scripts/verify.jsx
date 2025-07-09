const apiUrl = process.env.REACT_APP_API_URL;

export const VerifyUser = async (token) => {
    try {
        const response = await fetch(`${apiUrl}/auth/verify/${token}`, {
            method: "GET",
            credentials: "include",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        else alert('Верификация прошла успешно!')
        window.location.reload();

    } catch (error) {
        console.error("Error fetching user data:", error);
    } finally {
        
    }
    return null;
};