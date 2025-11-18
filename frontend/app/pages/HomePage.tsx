import { Box, Container, Stack } from "@mui/material";
import './HomePage.css'
import HistoryCard from "~/components/HistoryCard";
import Logo from "public/logo";
import carrotImg from './carrot.jpg'
import cucumberImg from './cucumber.jpg'
import potatoImg from './potato.jpg'

type Food = {
      name: string,
      weight: number,
      cal: number,
    }

const foodBoilerplate1: Food[] = [
  {
    name: "tomato",
    weight: 240,
    cal: 43
  },
  {
    name: "zucchini",
    weight: 300,
    cal: 85
  },
  {
    name: "potato",
    weight: 450,
    cal: 347
  },
  {
    name: "cauliflower",
    weight: 750,
    cal: 60
  },
  {
    name: "pumpkin",
    weight: 2100,
    cal: 560
  }
]

export default function Home() {
  return (
    <div className="homepage">
      <div className="content">
        <div className="top-section">
          <div className="logo-desc">
            <div className="logo">
              <span>Visi</span>
                <span>Meal</span>
            </div>
            <div className="desc">
              Recipes searching app based on Computer Vision
            </div>
            
          </div>

          <div className="short-history">
            <h3 className="block-header">Your Last Carts</h3>
            <div className="short-history-list">
                <HistoryCard 
                images={["prod4.jpg", "prod5.jpg"]}
                food={foodBoilerplate1}
                link={"nowhere"}
                />
                <HistoryCard 
                images={["prod1.jpg", "prod2.jpg", "prod3.jpg"]}
                food={foodBoilerplate1}
                link={"nowhere"}
                />
                <HistoryCard 
                images={["prod6.jpg"]}
                food={foodBoilerplate1}
                link={"nowhere"}
                />
                <HistoryCard 
                images={["prod6.jpg"]}
                food={foodBoilerplate1}
                link={"nowhere"}
                />
                <HistoryCard 
                images={["prod6.jpg"]}
                food={foodBoilerplate1}
                link={"nowhere"}
                />
            </div>
          </div>
        </div>

        <div className="recipes-examples">
          <div className="image-wrapper">
            <img src={"casserole.jpg"} />
            </div>
          <div className="image-wrapper">
            <img src={"hamandpotato.jpg"} />
            </div>
          <div className="image-wrapper">
            <img src={"jarkoe.jpg"} />
            </div>
          <div className="image-wrapper">
            <img src={"macandcheese.jpg"} />
            </div>
          <div className="image-wrapper">
            <img src={"salat.jpg"} />
          </div>
          <div className="image-wrapper">
            <img src={"kitayskaya-chicken.jpg"} />
          </div>
          <div className="image-wrapper">
            <img src={"lemon-pie.jpg"} />
          </div>
        </div>
        
        <div className="changelog">
            <h3 className="block-header">Changelog</h3>
            <div className="changelog-list">
                <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Corporis, obcaecati. Accusantium earum doloremque officiis sed expedita accusamus repudiandae placeat explicabo nisi veniam eveniet quas nesciunt, obcaecati saepe. A, atque tempore.</p>
                <p>Voluptatum illo officiis quod, ad aut aperiam ullam sequi! Doloremque reprehenderit hic corrupti earum? Reprehenderit sunt ratione cupiditate quo rem temporibus libero minus commodi assumenda! Error vero inventore porro molestias.</p>
                <p>Distinctio libero animi reprehenderit dicta. Rerum aliquid, reprehenderit cumque ipsa autem maiores natus commodi nostrum harum incidunt consequuntur dolor, maxime mollitia. Praesentium optio numquam doloribus deserunt at doloremque vitae vero!</p>
                <p>Praesentium, eveniet reprehenderit. Voluptatibus vitae ullam sunt tempora deserunt porro modi repellendus assumenda dolor! Suscipit eos, quo iste voluptate atque soluta, itaque numquam, ullam earum dolor recusandae laboriosam sapiente aspernatur.</p>
                <p>Enim similique nulla, eligendi consequuntur rem beatae ducimus perspiciatis. Eos quisquam quas unde nulla ducimus impedit eveniet dolore, quae, minus est quasi ratione amet maiores porro natus, dignissimos tempore deleniti.</p>
            </div>
        </div>
      </div>
    </div>
  )
}


