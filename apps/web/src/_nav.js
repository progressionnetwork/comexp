import {
  cibApache,
  cibBuffer,
  cibGithub,
  cilBuilding,
  cilFile,
  cilFlower,
  cilIndentIncrease,
  cilNotes,
  cilSpeedometer,
  cilSpreadsheet,
} from '@coreui/icons'
import CIcon from '@coreui/icons-react'
import { CNavItem, CNavTitle } from '@coreui/react'

const _nav = [
  {
    component: CNavItem,
    name: 'Новое планирование',
    to: '/plan',
    icon: <CIcon icon={cilSpeedometer} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Список планирования',
    to: '/plans',
    icon: <CIcon icon={cilSpeedometer} customClassName="nav-icon" />,
  },
  {
    component: CNavTitle,
    name: 'Данные',
  },
  {
    component: CNavItem,
    name: 'Строения',
    to: '/building',
    icon: <CIcon icon={cilBuilding} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Инциденты',
    to: '/incident',
    icon: <CIcon icon={cilSpreadsheet} customClassName="nav-icon" />,
  },
  {
    component: CNavTitle,
    name: 'Источники данных',
  },
  {
    component: CNavItem,
    name: 'Файлы',
    to: '/files',
    icon: <CIcon icon={cilFile} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'API',
    to: '/api',
    icon: <CIcon icon={cilIndentIncrease} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Apache Kafka (инциденты)',
    to: '/kafka',
    icon: <CIcon icon={cibApache} customClassName="nav-icon" />,
  },
  {
    component: CNavTitle,
    name: 'Справочники',
  },
  {
    component: CNavItem,
    name: 'Источники событий (системы)',
    to: '/source_system',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Виды работ',
    to: '/worktype',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Материалы стен',
    to: '/wall_material',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Материалы кровли',
    to: '/roof_material',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Категории МКД',
    to: '/category_mkd',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Серии проектов',
    to: '/project_series',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Очередность уборки кровли',
    to: '/queue_clean',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Статусы управления МКД',
    to: '/status_manage_mkd',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Статусы МКД',
    to: '/status_mkd',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Типы жилищного фонда',
    to: '/type_building',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Виды социальных объектов',
    to: '/type_social',
    icon: <CIcon icon={cilNotes} customClassName="nav-icon" />,
  },
  {
    component: CNavTitle,
    name: 'Репозиторий',
  },
  {
    component: CNavItem,
    name: 'Github',
    to: 'https://github.com/progressionnetwork/comexp',
    icon: <CIcon icon={cibGithub} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'API',
    to: 'https://api.comexp.intellectg.ru/docs/',
    icon: <CIcon icon={cibBuffer} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Flower (мониторинг задач)',
    to: 'https://dashboard.comexp.intellectg.ru/',
    icon: <CIcon icon={cilFlower} customClassName="nav-icon" />,
  },
]

export default _nav
