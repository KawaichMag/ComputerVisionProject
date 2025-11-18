import { Card, type CardProps } from '@mui/material'
import React from 'react'
import './HistoryCard.css'
import { NavLink } from 'react-router'
import ProductCard from './ProductCard'

interface CardsCollageProps {
    images: string[],
}

function CardsCollage( { images } : CardsCollageProps ) {
    return (
        <div className='cards-collage'>
            {images.map((item, index) => {
                return <img key={index} src={item}/>
            })}
        </div>
    )
}

type HistoryCardProps = CardsCollageProps & {
  food: {
      name: string,
      weight: number,
      cal: number,
    }[],
  link: string
};

export default function HistoryCard( props : HistoryCardProps) {
  return (
    <div className='history-card'>
      <CardsCollage images={props.images}/>
      <div className="product-cards">
        {props.food.map( (item, index) => {
          return (
            <ProductCard name={item.name} weight={item.weight} cal={item.cal} />
          )
        })}
      </div>
      
      <NavLink to={props.link}>
        Move to
      </NavLink>
    </div>
  )
}
