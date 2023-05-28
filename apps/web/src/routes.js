import React from 'react'
const Plan = React.lazy(() => import('./views/plan/Plan'))
const Files = React.lazy(() => import('./views/files/File'))
const Building = React.lazy(() => import('./views/building/Building'))
const FormList = React.lazy(() => import('./views/dicts/FormList'))
const SourceSystem = React.lazy(() => import('./views/sourceEvent/SourceEvent'))
const Incident = React.lazy(() => import('./views/incident/Incident'))
const API = React.lazy(() => import('./views/api/API'))
const Kafka = React.lazy(() => import('./views/kafka/Kafka'))
const Login = React.lazy(() => import('./views/pages/login/Login'))
const Page404 = React.lazy(() => import('./views/pages/page404/Page404'))
const Page500 = React.lazy(() => import('./views/pages/page500/Page500'))

const routes = [
  { path: '/', exact: true, name: 'Главная' },
  { path: '/plan', name: 'Плнирование', element: Plan },
  { path: '/files', name: 'Файлы данных', element: Files },
  { path: '/building', name: 'Строения', element: Building },
  { path: '/worktype', name: 'Виды работ', element: FormList },
  { path: '/wall_material', name: 'Матриалы стен', element: FormList },
  { path: '/roof_material', name: 'Матриалы кровли', element: FormList },
  { path: '/category_mkd', name: 'Категории МКД', element: FormList },
  { path: '/project_series', name: 'Серии проектов', element: FormList },
  { path: '/queue_clean', name: 'Очередность уборки кровли', element: FormList },
  { path: '/status_manage_mkd', name: 'Статусы управления МКД', element: FormList },
  { path: '/status_mkd', name: 'Статусы МКД', element: FormList },
  { path: '/type_building', name: 'Типы жилищного фонда', element: FormList },
  { path: '/type_social', name: 'Виды социальных объектов', element: FormList },
  { path: '/source_system', name: 'Источники событий', element: SourceSystem },
  { path: '/incident', name: 'Инциденты', element: Incident },
  { path: '/api', name: 'Источники данных: API', element: API },
  { path: '/kafka', name: 'Источники данных: Kafka', element: Kafka },
  { path: '/login', name: 'Вход', element: Login },
  { path: '/404', name: 'Ошибка 404', element: Page404 },
  { path: '/500', name: 'Ошибка 500', element: Page500 },
]

export default routes
