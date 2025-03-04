import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const PlaytimeChart = () => {
  const [games, setGames] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get('http://127.0.0.1:5000/api/games/123456789');  // 替换为真实 Steam ID
      setGames(response.data.response.games);
    };
    fetchData();
  }, []);

  const chartData = {
    labels: games.map((game) => game.name),
    datasets: [
      {
        label: 'Playtime (hours)',
        data: games.map((game) => Math.floor(game.playtime_forever / 60)),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };

  return (
    <div>
      <h2>Playtime Chart</h2>
      <Bar data={chartData} />
    </div>
  );
};

export default PlaytimeChart;