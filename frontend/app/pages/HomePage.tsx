import { Box, Container, Stack } from "@mui/material";
import './HomePage.css'

export default function Home() {
  return (
    <div className="homepage">
      <div className="content">
        <div className="top-section">
          <div className="logo-desc">
            <h2>Logo & Desc</h2>
          </div>

          <div className="short-history">
            <h2>History</h2>
            <div className="short-history-list">
                <p>hist exmpl.</p>
                <p>hist exmpl.</p>
                <p>hist exmpl.</p>
            </div>
          </div>
        </div>

        <div className="recipes-examples">
            <p>Recipe Exp</p>
            <p>Recipe Exp</p>
            <p>Recipe Exp</p>
            <p>Recipe Exp</p>
            <p>Recipe Exp</p>
        </div>
        
        <div className="changelog">
            <h3>Changelog</h3>
            <div className="changelog-list">
                <p>Cangelog exmpl</p>
            </div>
        </div>
      </div>
    </div>
  )
}


