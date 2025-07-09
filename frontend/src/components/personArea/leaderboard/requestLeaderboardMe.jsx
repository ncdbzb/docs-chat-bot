import { useState, useEffect } from "react";

export const useRequestLeaderboardMe = () => {
  const apiUrl = process.env.REACT_APP_API_URL;
  const [userData, setUserData] = useState({ datapk_itm: [], datapk: [] });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(`${apiUrl}/contest/leaderboard_me`, {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setUserData(data);
      } catch (error) {
        console.error("Error fetching user data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUserData();
  }, [apiUrl]);

  return { userData, isLoading }
};
