import { TextField } from '@mui/material';
import MuiAutocomplete, { createFilterOptions } from '@mui/material/Autocomplete';
import styles from './Autocomplete.module.scss'
import { IOption } from '../../utils';
import clsx from 'clsx';
import { ComponentProps } from 'react';

interface IAutocomplete<T> extends ComponentProps<"span"> {
  value?: IOption<T>
  setValue: (val: IOption<T> | undefined) => void
  options: IOption<T>[]
  label: string
  className?: string
  style?: Object
  onFocus?: () => void
  onBlur?: () => void
  disabled?: boolean
}

export function Autocomplete<T=string>(props: IAutocomplete<T>)  {
  const {value, setValue, label, options, className, style, onFocus, onBlur, disabled} = props
  
  return (
    <MuiAutocomplete
      value={value}
      onChange={(_e, val) => {
        if (val) {
          setValue(val)
        }
      }}
      options={options}
      renderInput={(params) => <TextField {...params} label={label} />}
      className={clsx(styles.root, className)}
      style={style}
      disabled={disabled}
    />
  )
}