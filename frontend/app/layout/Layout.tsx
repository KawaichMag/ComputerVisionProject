import './Layout.css'
import { NavLink, Outlet } from 'react-router'
import { useTheme } from 'app/contexts/ThemeContext';

export default function Layout() {
  const {theme, toggleTheme} = useTheme();

  console.log(theme);

  return (
    <>
        <div className="layout">
            <div className="navigation">
                <NavLink to={""}>Home Page</NavLink>
                <NavLink to={"/recipe-search"}>Recipes Search</NavLink>
                <NavLink to={"/chard"}>My Chart</NavLink>
            </div>
        </div>
        <div className="page-content">
            <Outlet/>
        </div>
    </>
  )
}
