import { createSlice } from '@reduxjs/toolkit'

const showSlice = createSlice({
  name: 'sidebarShow',
  initialState: {
    show: true,
  },
  reducers: {
    toggleSidebarShow(state = this.initialState, action) {
      state.show = !action.payload
    },
  },
})

export const { toggleSidebarShow } = showSlice.actions

export default showSlice.reducer
