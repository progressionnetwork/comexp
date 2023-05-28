import {
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
import { Map, YMaps } from 'react-yandex-maps'
import { setEndDate, setSource, setStartDate, setTypeFund } from 'src/redux/dashboardFilter'
import API from 'src/utils/Api'

const data_initial = {
  works: [
    {
      id: 29,
      date: '2022-07-15',
      address:
        'Российская Федерация, город Москва, внутригородская территория муниципальный округ Богородское, Ивантеевская улица, дом 1, корпус 6',
      work_type: {
        is_kr: true,
        id: 29,
        name: 'замена лифтового оборудования',
      },
    },
    {
      id: 30,
      date: '2022-07-15',
      address:
        'Российская Федерация, город Москва, внутригородская территория муниципальный округ Богородское, Ивантеевская улица, дом 1, корпус 6',
      work_type: {
        is_kr: true,
        id: 29,
        name: 'замена лифтового оборудования',
      },
    },
    {
      id: 31,
      date: '2022-07-15',
      address:
        'Российская Федерация, город Москва, внутригородская территория муниципальный округ Богородское, Ивантеевская улица, дом 1, корпус 6',
      work_type: {
        is_kr: true,
        id: 29,
        name: 'замена лифтового оборудования',
      },
    },
  ],
  incidents: [
    {
      name: 'Нарушение в работе  АГВ',
      id: 7057,
      date: '2022-07-15',
      address:
        'Российская Федерация, город Москва, внутригородская территория муниципальный округ Богородское, Ивантеевская улица, дом 1, корпус 6',
      source: {
        name: 'MOS_GAS',
        id: 1,
      },
    },
    {
      name: 'Нарушение в работе  АГВ',
      id: 7058,
      address:
        'Российская Федерация, город Москва, внутригородская территория муниципальный округ Богородское, Ивантеевская улица, дом 1, корпус 6',
      date: '2022-07-15',
      source: {
        name: 'MOS_GAS',
        id: 1,
      },
    },
  ],
}

const ResultTable = ({ title, columns, rows }) => {
  const [selectedRows, setSelectedRows] = useState([])
  const [toggleCleared, setToggleCleared] = useState(false)
  const [data, setData] = useState(rows)

  const handleRowSelected = useCallback((state) => {
    setSelectedRows(state.selectedRows)
  }, [])

  const contextActions = useMemo(() => {
    const handleDelete = () => {
      setToggleCleared(!toggleCleared)
      setData(differenceBy(data, selectedRows, 'id'))
    }

    return (
      <CButton key="delete" onClick={handleDelete} style={{ backgroundColor: 'red' }} icon>
        Удалить
      </CButton>
    )
  }, [data, selectedRows, toggleCleared])

  return (
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
  )
}

const Plan = () => {
  const [listTypeFund, setListTypeFund] = useState([])
  const [listSource, setListSource] = useState([])
  const [street, setStreet] = useState('Перовская')
  const [activeKey, setActiveKey] = useState(1)
  const [mapCenter, setMapCenter] = useState({ center: [55.75, 37.57], zoom: 18 })
  const [result, setResult] = useState(data_initial)

  const dispatch = useDispatch()
  const typeFund = useSelector((state) => state.dashboard.filter.typeFund)
  const source = useSelector((state) => state.dashboard.filter.source)
  const startDate = useSelector((state) => state.dashboard.filter.startDate)
  const endDate = useSelector((state) => state.dashboard.filter.endDate)
  const YM_TOKEN = process.env.REACT_APP_YM_TOKEN
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

  const handleMakeData = () => {
    console.log(typeFund, source, street)
  }

  useEffect(() => {
    get_type_fund()
    get_source()
  }, [])
  return (
    <>
      <CCard className="mb-5">
        <CCardHeader>
          <h4 id="traffic" className="card-title mb-0">
            Сформировать список для плнирования
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
                options={[...listTypeFund, { label: 'не указывать', value: 0 }]}
                defaultValue={typeFund}
                onChange={(event) => dispatch(setTypeFund(event.target.value))}
                style={{ maxWidth: '200px', width: '200px' }}
              />
            </CCol>
            <CCol xs={12}>
              <h6>Источник</h6>
              <CFormSelect
                options={[...listSource]}
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
      <CCard className="mb-5">
        <CCardHeader>
          <h4 id="traffic" className="card-title mb-0">
            Результат
          </h4>
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
                      name: 'Дата',
                      selector: (row) => row.date,
                    },
                    {
                      name: 'Адрес',
                      selector: (row) => row.address,
                    },
                    {
                      name: 'Наименование',
                      selector: (row) => row.work_type.name,
                    },
                  ]}
                  rows={result['works']}
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
                      name: 'Дата',
                      selector: (row) => row.date,
                    },
                    {
                      name: 'Адрес',
                      selector: (row) => row.address,
                    },
                    {
                      name: 'Наименование',
                      selector: (row) => row.name,
                    },
                    {
                      name: 'Источник',
                      selector: (row) => row.source.name,
                    },
                  ]}
                  rows={result['incidents']}
                />
              </CContainer>
            </CTabPane>
          </CTabContent>
        </CCardBody>
      </CCard>
      <CCard className="mb-5">
        <CCardHeader>
          <h4 id="traffic" className="card-title mb-0">
            Карта
          </h4>
        </CCardHeader>
        <CCardBody className="col justify-content-center">
          <YMaps
            query={{
              ns: 'use-load-option',
              apikey: YM_TOKEN,
              load: 'geocode',
            }}
            on
          >
            <div>
              <Map state={mapCenter} style={{ width: '100%', height: '400px' }}></Map>
            </div>
          </YMaps>
        </CCardBody>
      </CCard>
    </>
  )
}

export default Plan
