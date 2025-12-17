import React, { useState } from 'react';
import {
  Box,
  Container,
  Heading,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  Button,
  useColorModeValue,
  VStack,
  HStack,
  Text,
  Spinner,
  Center,
} from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import { adminService } from '@/services/admin.service';

const Admin: React.FC = () => {
  const cardBg = useColorModeValue('white', 'gray.700');

  const { data: overview, isLoading: overviewLoading } = useQuery({
    queryKey: ['admin-overview'],
    queryFn: adminService.getAnalyticsOverview,
  });

  const { data: users, isLoading: usersLoading } = useQuery({
    queryKey: ['admin-users'],
    queryFn: () => adminService.getAllUsers(0, 50),
  });

  const { data: orgAnalytics, isLoading: orgLoading } = useQuery({
    queryKey: ['admin-org-analytics'],
    queryFn: () => adminService.getOrganizationAnalytics(0, 20),
  });

  const { data: docStats, isLoading: docStatsLoading } = useQuery({
    queryKey: ['admin-doc-stats'],
    queryFn: adminService.getDocumentStats,
  });

  if (overviewLoading) {
    return (
      <Center h="50vh">
        <Spinner size="xl" />
      </Center>
    );
  }

  return (
    <Container maxW="container.xl" py={8}>
      <VStack align="stretch" spacing={8}>
        <Heading size="lg">Admin Dashboard</Heading>

        {/* Overview Stats */}
        <SimpleGrid columns={{ base: 1, md: 4 }} spacing={6}>
          <Box bg={cardBg} p={6} borderRadius="lg" shadow="md" borderWidth="1px">
            <Stat>
              <StatLabel>Total Organizations</StatLabel>
              <StatNumber>{overview?.total_organizations || 0}</StatNumber>
              <StatHelpText>Active organizations</StatHelpText>
            </Stat>
          </Box>
          <Box bg={cardBg} p={6} borderRadius="lg" shadow="md" borderWidth="1px">
            <Stat>
              <StatLabel>Total Users</StatLabel>
              <StatNumber>{overview?.total_users || 0}</StatNumber>
              <StatHelpText>Registered users</StatHelpText>
            </Stat>
          </Box>
          <Box bg={cardBg} p={6} borderRadius="lg" shadow="md" borderWidth="1px">
            <Stat>
              <StatLabel>Total Documents</StatLabel>
              <StatNumber>{overview?.total_documents || 0}</StatNumber>
              <StatHelpText>Uploaded documents</StatHelpText>
            </Stat>
          </Box>
          <Box bg={cardBg} p={6} borderRadius="lg" shadow="md" borderWidth="1px">
            <Stat>
              <StatLabel>Total Conversations</StatLabel>
              <StatNumber>{overview?.total_conversations || 0}</StatNumber>
              <StatHelpText>Chat sessions</StatHelpText>
            </Stat>
          </Box>
        </SimpleGrid>

        {/* Tabs for detailed views */}
        <Box bg={cardBg} borderRadius="lg" shadow="md" borderWidth="1px" p={6}>
          <Tabs>
            <TabList>
              <Tab>Users</Tab>
              <Tab>Organizations</Tab>
              <Tab>Documents</Tab>
            </TabList>

            <TabPanels>
              {/* Users Tab */}
              <TabPanel>
                {usersLoading ? (
                  <Center py={8}>
                    <Spinner />
                  </Center>
                ) : (
                  <Table variant="simple">
                    <Thead>
                      <Tr>
                        <Th>Name</Th>
                        <Th>Email</Th>
                        <Th>Role</Th>
                        <Th>Status</Th>
                        <Th>Last Login</Th>
                        <Th>Actions</Th>
                      </Tr>
                    </Thead>
                    <Tbody>
                      {users?.map((user) => (
                        <Tr key={user.id}>
                          <Td>{user.full_name}</Td>
                          <Td>{user.email}</Td>
                          <Td>
                            <Badge colorScheme={user.role === 'admin' ? 'purple' : 'blue'}>
                              {user.role}
                            </Badge>
                          </Td>
                          <Td>
                            <Badge colorScheme={user.is_active ? 'green' : 'red'}>
                              {user.is_active ? 'Active' : 'Inactive'}
                            </Badge>
                          </Td>
                          <Td>
                            {user.last_login
                              ? new Date(user.last_login).toLocaleDateString()
                              : 'Never'}
                          </Td>
                          <Td>
                            <Button size="sm" variant="ghost">
                              Manage
                            </Button>
                          </Td>
                        </Tr>
                      ))}
                    </Tbody>
                  </Table>
                )}
              </TabPanel>

              {/* Organizations Tab */}
              <TabPanel>
                {orgLoading ? (
                  <Center py={8}>
                    <Spinner />
                  </Center>
                ) : (
                  <Table variant="simple">
                    <Thead>
                      <Tr>
                        <Th>Name</Th>
                        <Th>Tier</Th>
                        <Th>Users</Th>
                        <Th>Documents</Th>
                        <Th>Conversations</Th>
                        <Th>Status</Th>
                      </Tr>
                    </Thead>
                    <Tbody>
                      {orgAnalytics?.map((org) => (
                        <Tr key={org.id}>
                          <Td>{org.name}</Td>
                          <Td>
                            <Badge
                              colorScheme={
                                org.tier === 'enterprise'
                                  ? 'purple'
                                  : org.tier === 'pro'
                                  ? 'blue'
                                  : 'gray'
                              }
                            >
                              {org.tier}
                            </Badge>
                          </Td>
                          <Td>{org.users}</Td>
                          <Td>{org.documents}</Td>
                          <Td>{org.conversations}</Td>
                          <Td>
                            <Badge colorScheme={org.is_active ? 'green' : 'red'}>
                              {org.is_active ? 'Active' : 'Inactive'}
                            </Badge>
                          </Td>
                        </Tr>
                      ))}
                    </Tbody>
                  </Table>
                )}
              </TabPanel>

              {/* Documents Tab */}
              <TabPanel>
                {docStatsLoading ? (
                  <Center py={8}>
                    <Spinner />
                  </Center>
                ) : (
                  <VStack align="stretch" spacing={4}>
                    <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                      <Box p={4} bg="gray.50" borderRadius="md">
                        <Text fontWeight="bold">Total Documents</Text>
                        <Text fontSize="2xl">{docStats?.total_documents || 0}</Text>
                      </Box>
                      <Box p={4} bg="gray.50" borderRadius="md">
                        <Text fontWeight="bold">Total Size</Text>
                        <Text fontSize="2xl">{docStats?.total_size_mb || 0} MB</Text>
                      </Box>
                      <Box p={4} bg="gray.50" borderRadius="md">
                        <Text fontWeight="bold">Average Size</Text>
                        <Text fontSize="2xl">
                          {docStats?.total_documents
                            ? (docStats.total_size_mb / docStats.total_documents).toFixed(2)
                            : 0}{' '}
                          MB
                        </Text>
                      </Box>
                    </SimpleGrid>
                    {docStats?.status_breakdown && (
                      <Box>
                        <Text fontWeight="bold" mb={2}>
                          Status Breakdown
                        </Text>
                        <HStack spacing={4}>
                          {Object.entries(docStats.status_breakdown).map(([status, count]) => (
                            <Badge key={status} colorScheme="blue" p={2}>
                              {status}: {count as number}
                            </Badge>
                          ))}
                        </HStack>
                      </Box>
                    )}
                  </VStack>
                )}
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Box>
      </VStack>
    </Container>
  );
};

export default Admin;

