import {
  CBadge,
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CFormSelect,
  CNav,
  CNavItem,
  CNavLink,
  CTabContent,
  CTabPane,
} from '@coreui/react'
import ru from 'date-fns/locale/ru'
import differenceBy from 'lodash/differenceBy'
import { useCallback, useEffect, useMemo, useState } from 'react'
import DataTable from 'react-data-table-component'
import DatePicker from 'react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import { useDispatch, useSelector } from 'react-redux'
import { useParams } from 'react-router-dom'
import { Clusterer, Map, Placemark, YMaps } from 'react-yandex-maps'
import { setEndDate, setSource, setStartDate, setTypeFund } from 'src/redux/dashboardFilter'
import API from 'src/utils/Api'

const ResultTable = ({ title, columns, rows, statusPredict }) => {
  const [selectedRows, setSelectedRows] = useState([])
  const [toggleCleared, setToggleCleared] = useState(false)
  const [data, setData] = useState(rows)
  const handleRowSelected = useCallback((state) => {
    setSelectedRows(state.selectedRows)
  }, [])

  useEffect(() => {
    setData(rows)
  }, [rows])

  const contextActions = useMemo(() => {
    const handleDelete = () => {
      setToggleCleared(!toggleCleared)
      console.log(selectedRows)
      setData(differenceBy(data, selectedRows, 'id'))
      selectedRows.map((elem) => {
        if (title == 'Предсказанные работы') {
          API.delete(`/plan_works/${elem.id}`)
        } else {
          API.delete(`/plan_events/${elem.id}`)
        }
      })
    }

    return (
      <CButton key="delete" onClick={handleDelete} style={{ backgroundColor: 'red' }} icon>
        Удалить
      </CButton>
    )
  }, [data, selectedRows, toggleCleared])

  return (
    <>
      <DataTable
        title={title}
        columns={columns}
        data={data}
        selectableRows
        contextActions={contextActions}
        onSelectedRowsChange={handleRowSelected}
        clearSelectedRows={toggleCleared}
        pagination
      />
      Для удаления выберите необходимые строки
    </>
  )
}
const BuildingOnMaps = ({ addresses }) => {
  const [mapCenter, setMapCenter] = useState({ center: [55.787715, 37.775631], zoom: 12 })
  const [mapPoints, setMapPoints] = useState([])
  const YM_TOKEN = process.env.REACT_APP_YM_TOKEN
  const geocode = async (ymaps) => {
    console.log(ymaps)
    let _mapPoint = []
    console.log(addresses)
    addresses.map(async (elem) => {
      const geoObj = await ymaps.geocode(`г. Москва, ${elem}`)
      _mapPoint.push(geoObj.geoObjects.get(0).geometry.getCoordinates())
    })
    setMapCenter({ center: _mapPoint[0], zoom: 12 })
    setMapPoints(_mapPoint)
    console.log(mapCenter)
  }
  return (
    <YMaps
      query={{
        ns: 'use-load-option',
        apikey: YM_TOKEN,
        load: 'geocode',
      }}
    >
      <Map
        state={mapCenter}
        defaultState={mapCenter}
        style={{ width: '100%', height: '400px' }}
        onLoad={geocode}
      >
        <Clusterer
          options={{
            preset: 'islands#invertedVioletClusterIcons',
            groupByCoordinates: false,
          }}
        >
          {mapPoints &&
            mapPoints.map((elem) => {
              return <Placemark key={elem[0] + elem[1]} geometry={elem} />
            })}
        </Clusterer>
      </Map>
    </YMaps>
  )
}
const Plan = () => {
  const params = useParams()

  const [listTypeFund, setListTypeFund] = useState([])
  const [listSource, setListSource] = useState([])
  const [street, setStreet] = useState('Алтайская')
  const [activeKey, setActiveKey] = useState(1)
  const [result, setResult] = useState({ works: [], incidents: [] })
  const [planId, setPlanId] = useState(params.id ? params.id : 0)
  const [statusPredict, setStatusPredict] = useState(false)
  const [addresses, setAddresses] = useState(false)

  const dispatch = useDispatch()
  const typeFund = useSelector((state) => state.dashboard.filter.typeFund)
  const source = useSelector((state) => state.dashboard.filter.source)
  const startDate = useSelector((state) => state.dashboard.filter.startDate)
  const endDate = useSelector((state) => state.dashboard.filter.endDate)

  const get_type_fund = async () => {
    const response = await API.get(`type_building/?offset=0&limit=100`)
    setListTypeFund(
      response.data.map((elem) => {
        return { label: elem.name, value: elem.id }
      }),
    )
  }
  const get_source = async () => {
    const response = await API.get(`sourcesystem/?offset=0&limit=100`)
    setListSource(
      response.data.map((elem) => {
        return { label: elem.name, value: elem.id }
      }),
    )
  }

  const handleMakeData = async () => {
    const response = await API.post(
      `plan/?street=${street}&type_fund_id=${typeFund}&sorucesystem_id=${source}&start_date=${startDate}&end_date=${endDate}`,
    )
    setPlanId(response.data.id)
  }

  const updatePredict = async () => {
    if (planId !== 0) {
      const response = await API.get(`plan/${planId}`)
      setResult({ works: response.data.works, incidents: response.data.events })
      const works = response.data.works
      const incidents = response.data.events
      let _addresses = []
      works.map((elem) => {
        if (!_addresses.includes(elem.building.name)) {
          _addresses.push(elem.building.name)
        }
      })
      incidents.map((elem) => {
        if (!_addresses.includes(elem.building.name)) {
          _addresses.push(elem.building.name)
        }
      })
      setAddresses(_addresses)
      setStatusPredict(Boolean(response.data.status))
    }
  }

  useEffect(() => {
    get_type_fund()
    get_source()
  }, [])

  useEffect(() => {
    const timeout = setTimeout(() => {
      updatePredict()
    }, 10)
    return () => clearTimeout(timeout)
  }, [planId])
  return (
    <>
      {planId === 0 && (
        <CCard className="mb-5">
          <CCardHeader>
            <h4 id="traffic" className="card-title mb-0">
              Сформировать список для планирования
            </h4>
          </CCardHeader>
          <CCardBody className="col justify-content-center">
            <CForm className="m-1 row row-cols-lg-auto g-3 align-items-end  justify-content-between">
              <CCol xs={12}>
                <h6>Улица</h6>
                <CFormInput
                  defaultValue={street}
                  onChange={(event) => setStreet(event.target.value)}
                  style={{ maxWidth: '200px', width: '200px' }}
                />
              </CCol>
              <CCol xs={12}>
                <h6>Тип фонда</h6>
                <CFormSelect
                  options={[
                    'Выберите тип...',
                    ...listTypeFund,
                    { label: 'не указывать', value: 0 },
                  ]}
                  defaultValue={typeFund}
                  onChange={(event) => dispatch(setTypeFund(event.target.value))}
                  style={{ maxWidth: '200px', width: '200px' }}
                />
              </CCol>
              <CCol xs={12}>
                <h6>Источник</h6>
                <CFormSelect
                  options={['Выберите источник...', ...listSource]}
                  defaultValue={source}
                  onChange={(event) => dispatch(setSource(event.target.value))}
                  style={{ maxWidth: '200px', width: '200px' }}
                />
              </CCol>
              <CCol xs={12}>
                <h6>Начало периода</h6>
                <DatePicker
                  className="form-control"
                  locale={ru}
                  selected={startDate}
                  onChange={(date) => dispatch(setStartDate(date.getTime()))}
                  dateFormat="dd.MM.yyyy"
                  style={{ maxWidth: '200px', width: '200px' }}
                />
              </CCol>
              <CCol xs={12}>
                <h6>Окончание периода</h6>
                <DatePicker
                  className="form-control"
                  locale={ru}
                  selected={endDate}
                  onChange={(date) => dispatch(setEndDate(date.getTime()))}
                  dateFormat="dd.MM.yyyy"
                  style={{ maxWidth: '200px', width: '200px' }}
                />
              </CCol>
              <CButton onClick={handleMakeData}>Сформировать</CButton>
            </CForm>
          </CCardBody>
        </CCard>
      )}
      {planId !== 0 && (
        <CCard className="mb-5">
          <CCardHeader>
            <h4 id="traffic" className="card-title mb-0">
              Результат
            </h4>
            {statusPredict && <CBadge color="success">Готово</CBadge>}
            {!statusPredict && <CBadge color="warning">В работе</CBadge>}
          </CCardHeader>
          <CCardBody className="col justify-content-center">
            <CNav variant="tabs" role="tablist">
              <CNavItem>
                <CNavLink
                  active={activeKey === 1}
                  onClick={() => setActiveKey(1)}
                  style={{ cursor: 'pointer' }}
                >
                  Работы
                </CNavLink>
              </CNavItem>
              <CNavItem>
                <CNavLink
                  active={activeKey === 2}
                  onClick={() => setActiveKey(2)}
                  style={{ cursor: 'pointer' }}
                >
                  Инциденты
                </CNavLink>
              </CNavItem>
              <CNavItem>
                <CNavLink
                  active={activeKey === 3}
                  onClick={() => setActiveKey(3)}
                  style={{ cursor: 'pointer' }}
                >
                  На карте
                </CNavLink>
              </CNavItem>
            </CNav>
            <CTabContent>
              <CTabPane role="tabpanel" aria-labelledby="home-tab" visible={activeKey === 1}>
                <CContainer fluid>
                  <ResultTable
                    title="Предсказанные работы"
                    columns={[
                      {
                        name: '#',
                        selector: (row) => row.id,
                        maxWidth: '100px',
                      },
                      {
                        name: 'Наименование',
                        selector: (row) => row.work.name,
                        wrap: true,
                      },
                      {
                        name: 'Адрес',
                        selector: (row) => row.building.name,
                      },
                      {
                        name: 'Дней до начала',
                        selector: (row) => row.start_day,
                      },
                      {
                        name: 'Дней до окончания',
                        selector: (row) => row.end_day,
                      },
                      {
                        name: 'Точность',
                        selector: (row) => row.acc,
                      },
                    ]}
                    rows={result['works']}
                    statusPredict={statusPredict}
                  />
                </CContainer>
              </CTabPane>
              <CTabPane role="tabpanel" aria-labelledby="profile-tab" visible={activeKey === 2}>
                <CContainer fluid>
                  <ResultTable
                    title="Предсказанные инциденты"
                    columns={[
                      {
                        name: '#',
                        selector: (row) => row.id,
                        maxWidth: '100px',
                      },
                      {
                        name: 'Наименование',
                        selector: (row) => row.event.name,
                        wrap: true,
                      },
                      {
                        name: 'Адрес',
                        selector: (row) => row.building.name,
                      },
                      {
                        name: 'Точность',
                        selector: (row) => row.acc,
                      },
                    ]}
                    rows={result['incidents']}
                    statusPredict={statusPredict}
                  />
                </CContainer>
              </CTabPane>
              <CTabPane role="tabpanel" aria-labelledby="map-tab" visible={activeKey === 3}>
                {addresses && <BuildingOnMaps addresses={addresses} />}
              </CTabPane>
            </CTabContent>
          </CCardBody>
        </CCard>
      )}
    </>
  )
}

export default Plan
