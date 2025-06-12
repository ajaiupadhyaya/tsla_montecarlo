import { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Heading,
  Text,
  Grid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  useColorModeValue,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from '@chakra-ui/react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export default function Home() {
  const [currentPrice, setCurrentPrice] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [monteCarlo, setMonteCarlo] = useState(null);
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [priceRes, histRes, metricsRes, monteCarloRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/stock/current`),
          axios.get(`${API_BASE_URL}/stock/historical`),
          axios.get(`${API_BASE_URL}/stock/metrics`),
          axios.get(`${API_BASE_URL}/stock/monte-carlo`),
        ]);

        setCurrentPrice(priceRes.data);
        setHistoricalData(histRes.data);
        setMetrics(metricsRes.data);
        setMonteCarlo(monteCarloRes.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 60000); // Update every minute
    return () => clearInterval(interval);
  }, []);

  return (
    <Container maxW="container.xl" py={8}>
      <Heading mb={8}>Tesla Stock Analysis</Heading>

      {currentPrice && (
        <Grid templateColumns="repeat(4, 1fr)" gap={6} mb={8}>
          <Stat
            px={4}
            py={5}
            bg={bgColor}
            rounded="lg"
            border="1px"
            borderColor={borderColor}
          >
            <StatLabel>Current Price</StatLabel>
            <StatNumber>${currentPrice.price?.toFixed(2)}</StatNumber>
            <StatHelpText>
              <StatArrow type={currentPrice.change >= 0 ? 'increase' : 'decrease'} />
              {currentPrice.change?.toFixed(2)}%
            </StatHelpText>
          </Stat>

          <Stat
            px={4}
            py={5}
            bg={bgColor}
            rounded="lg"
            border="1px"
            borderColor={borderColor}
          >
            <StatLabel>Volume</StatLabel>
            <StatNumber>{(currentPrice.volume / 1000000).toFixed(2)}M</StatNumber>
          </Stat>

          <Stat
            px={4}
            py={5}
            bg={bgColor}
            rounded="lg"
            border="1px"
            borderColor={borderColor}
          >
            <StatLabel>Market Cap</StatLabel>
            <StatNumber>${(currentPrice.market_cap / 1e9).toFixed(2)}B</StatNumber>
          </Stat>

          <Stat
            px={4}
            py={5}
            bg={bgColor}
            rounded="lg"
            border="1px"
            borderColor={borderColor}
          >
            <StatLabel>Volatility</StatLabel>
            <StatNumber>{(metrics?.volatility * 100).toFixed(2)}%</StatNumber>
          </Stat>
        </Grid>
      )}

      <Tabs variant="enclosed" mb={8}>
        <TabList>
          <Tab>Price History</Tab>
          <Tab>Monte Carlo Simulation</Tab>
          <Tab>Metrics</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <Box
              bg={bgColor}
              p={4}
              rounded="lg"
              border="1px"
              borderColor={borderColor}
              height="400px"
            >
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={historicalData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="Date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="Close"
                    stroke="#8884d8"
                    name="Closing Price"
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </TabPanel>

          <TabPanel>
            <Box
              bg={bgColor}
              p={4}
              rounded="lg"
              border="1px"
              borderColor={borderColor}
              height="400px"
            >
              <ResponsiveContainer width="100%" height="100%">
                <LineChart>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    data={monteCarlo?.mean_path}
                    stroke="#8884d8"
                    name="Mean Path"
                  />
                  <Line
                    type="monotone"
                    data={monteCarlo?.confidence_interval_95.upper}
                    stroke="#82ca9d"
                    name="95% Upper Bound"
                  />
                  <Line
                    type="monotone"
                    data={monteCarlo?.confidence_interval_95.lower}
                    stroke="#ffc658"
                    name="95% Lower Bound"
                  />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </TabPanel>

          <TabPanel>
            <Grid templateColumns="repeat(2, 1fr)" gap={6}>
              {metrics && Object.entries(metrics).map(([key, value]) => (
                <Stat
                  key={key}
                  px={4}
                  py={5}
                  bg={bgColor}
                  rounded="lg"
                  border="1px"
                  borderColor={borderColor}
                >
                  <StatLabel>{key.replace(/_/g, ' ').toUpperCase()}</StatLabel>
                  <StatNumber>
                    {typeof value === 'number'
                      ? value.toFixed(4)
                      : value}
                  </StatNumber>
                </Stat>
              ))}
            </Grid>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Container>
  );
} 