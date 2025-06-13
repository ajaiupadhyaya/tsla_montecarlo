import { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Heading,
  Text,
  VStack,
  HStack,
  Stat,
  StatLabel,
  StatHelpText,
  StatGroup,
  useColorMode,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  StatArrow,
  StatNumber,
  useColorModeValue,
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
  const { colorMode, toggleColorMode } = useColorMode();
  const bgColor = useColorModeValue('white', 'gray.800');
  const textColor = useColorModeValue('gray.800', 'white');
  const [currentPrice, setCurrentPrice] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [monteCarlo, setMonteCarlo] = useState(null);
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
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading as="h1" size="xl" mb={4}>
            Tesla Stock Analysis
          </Heading>
          <Text fontSize="lg" color={textColor}>
            Real-time analysis and predictions for Tesla stock
          </Text>
        </Box>

        <StatGroup>
          <Stat>
            <StatLabel>Current Price</StatLabel>
            <StatNumber>$0.00</StatNumber>
            <StatHelpText>
              <StatArrow type="increase" />
              0.00%
            </StatHelpText>
          </Stat>
        </StatGroup>

        <Tabs variant="enclosed">
          <TabList>
            <Tab>Price Chart</Tab>
            <Tab>Technical Analysis</Tab>
            <Tab>ML Predictions</Tab>
          </TabList>

          <TabPanels>
            <TabPanel>
              <Box h="400px" bg={bgColor} p={4} borderRadius="lg">
                {/* Price chart will go here */}
              </Box>
            </TabPanel>
            <TabPanel>
              <Box h="400px" bg={bgColor} p={4} borderRadius="lg">
                {/* Technical analysis will go here */}
              </Box>
            </TabPanel>
            <TabPanel>
              <Box h="400px" bg={bgColor} p={4} borderRadius="lg">
                {/* ML predictions will go here */}
              </Box>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
    </Container>
  );
} 