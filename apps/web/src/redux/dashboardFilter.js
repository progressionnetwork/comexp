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
      typeFund: 42875644,
      social: 0,
      source: 3,
      endDate: monthAgo(0),
      startDate: monthAgo(1),
    },
  },
  reducers: {
    setTypeFund(state, action) {
      state.filter.typeFund = action.payload
    },
    setSocial(state, action) {
      state.filter.social = action.payload
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

export const { setTypeFund, setSocial, setEndDate, setSource, setStartDate } =
  dashboardFilter.actions

export default dashboardFilter.reducer
