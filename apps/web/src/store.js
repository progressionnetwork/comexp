import { configureStore } from '@reduxjs/toolkit'
import dashboardFilter from './redux/dashboardFilter'
import sidebarShow from './redux/sidebar'

export default configureStore({
  reducer: { sidebar: sidebarShow, dashboard: dashboardFilter },
})
