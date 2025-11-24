import React from 'react'
import './PredictionCard.css'

export default function PredictionCard(props: {name: string, amount: number, weight: number, cal: number}) {

    return (
        <div className='predict-card'>
            <span className='predict-amount'>{props.amount}</span>
            <span className='predict-name'> {props.name}</span>
            <span className='predict-weight'> {props.weight}g</span>
            <span className='predict-cals'> {props.cal}cal</span>
        </div>
    )
}
