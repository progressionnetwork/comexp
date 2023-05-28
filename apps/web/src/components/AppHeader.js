import { cilMenu } from '@coreui/icons'
import CIcon from '@coreui/icons-react'
import {
  CContainer,
  CHeader,
  CHeaderBrand,
  CHeaderDivider,
  CHeaderNav,
  CHeaderToggler,
  CNavItem,
  CNavLink,
} from '@coreui/react'
import { useDispatch, useSelector } from 'react-redux'
import { toggleSidebarShow } from 'src/redux/sidebar'
import logo from '../assets/images/logo.png'
import { AppHeaderDropdown } from './header/index'
import { AppBreadcrumb } from './index'
const AppHeader = () => {
  const dispatch = useDispatch()
  const sidebarShow = useSelector((state) => state.sidebar.show)
  return (
    <CHeader position="sticky" className="mb-4">
      <CContainer fluid>
        <CHeaderToggler className="ps-1" onClick={() => dispatch(toggleSidebarShow(sidebarShow))}>
          <CIcon icon={cilMenu} size="lg" />
        </CHeaderToggler>
        <CHeaderBrand className="mx-auto d-md-none " to="/">
          <div className="d-flex align-items-center">
            <a href="/">
              <img src={logo} alt="Logo" style={{ width: '32px' }} className="m-3" />
            </a>
            <h5>Коммунальный эксперт</h5>
          </div>
        </CHeaderBrand>
        <CHeaderNav className="d-none d-md-flex me-auto">
          <CNavItem>
            <CNavLink style={{ cursor: 'pointer' }}>🎱 Переобучить модели</CNavLink>
          </CNavItem>
        </CHeaderNav>
        <CHeaderNav className="ms-3">
          <AppHeaderDropdown />
        </CHeaderNav>
      </CContainer>
      <CHeaderDivider />
      <CContainer fluid>
        <AppBreadcrumb />
      </CContainer>
    </CHeader>
  )
}

export default AppHeader
