import { createSlice } from '@reduxjs/toolkit'

const monthAgo = (count) => {
  let d = new Date()
  d.setMonth(d.getMonth() - count)
  return d.getTime()
}

const dashboardFilter = createSlice({
  name: 'dashboardSlice',
  initialState: {
    filter: {
      category: 0,
      source: 0,
      endDate: monthAgo(0),
      startDate: monthAgo(1),
    },
  },
  reducers: {
    setCategory(state, action) {
      state.filter.category = action.payload
    },
    setSource(state, action) {
      state.filter.source = action.payload
    },
    setStartDate(state, action) {
      state.filter.startDate = action.payload
    },
    setEndDate(state, action) {
      state.filter.endDate = action.payload
    },
  },
})

export const { setCategory, setEndDate, setSource, setStartDate } = dashboardFilter.actions

export default dashboardFilter.reducer
