import React from 'react'
import { useSelector } from 'react-redux'

import { CSidebar, CSidebarBrand, CSidebarNav } from '@coreui/react'

import SimpleBar from 'simplebar-react'
import 'simplebar/dist/simplebar.min.css'
import navigation from '../_nav'
import logo from '../assets/images/logo.png'
import { AppSidebarNav } from './AppSidebarNav'
const AppSidebar = () => {
  const sidebarShow = useSelector((state) => state.sidebar.show)
  return (
    <CSidebar position="fixed" size="lg" visible={sidebarShow}>
      <CSidebarBrand className="d-none d-md-flex" to="/">
        <a href="/">
          <img src={logo} alt="Logo" style={{ width: '64px' }} className="m-3" />
        </a>
        <h3>Коммунальный эксперт</h3>
      </CSidebarBrand>
      <CSidebarNav>
        <SimpleBar>
          <AppSidebarNav items={navigation} />
        </SimpleBar>
      </CSidebarNav>
    </CSidebar>
  )
}

export default React.memo(AppSidebar)
