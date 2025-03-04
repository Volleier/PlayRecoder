import React from 'react';
import { Link, Outlet } from 'react-router-dom';

const Dashboard = () => {
  return (
    <div>
      <h1>Dashboard</h1>
      <nav>
        <Link to="games">Games Table</Link>
        <Link to="playtime">Playtime Chart</Link>
      </nav>
      <Outlet />
    </div>
  );
};

export default Dashboard;