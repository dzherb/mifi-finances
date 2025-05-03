import MuiBtn, { ButtonProps } from '@mui/material/Button';
import { FC } from 'react';
import clsx from 'clsx';
import styles from './Button.module.scss'


export const Button: FC<ButtonProps> = (props) => {
  const {children, className, style, onClick, ...args} = props

  return (
    <MuiBtn 
      variant="contained"
      className={clsx(className, styles.btn )}
      style={style}
      onClick={onClick}
      {...args}
    >
      {children}
    </MuiBtn>
  )
}
