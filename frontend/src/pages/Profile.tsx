import React, { useState } from 'react';
import {
  Box,
  Container,
  Heading,
  VStack,
  FormControl,
  FormLabel,
  Input,
  Button,
  useColorModeValue,
  Avatar,
  HStack,
  Text,
  Divider,
} from '@chakra-ui/react';
import { useAuth } from '@/contexts/AuthContext';

const Profile: React.FC = () => {
  const { user, refetchUser } = useAuth();
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [isLoading, setIsLoading] = useState(false);

  const cardBg = useColorModeValue('white', 'gray.700');

  const handleUpdateProfile = async () => {
    setIsLoading(true);
    // TODO: Implement profile update
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  };

  return (
    <Container maxW="container.md" py={8}>
      <VStack align="stretch" spacing={8}>
        <Heading size="lg">Profile</Heading>

        <Box bg={cardBg} p={8} borderRadius="lg" shadow="md" borderWidth="1px">
          <VStack align="stretch" spacing={6}>
            <HStack spacing={4}>
              <Avatar size="xl" name={user?.full_name} />
              <VStack align="start" spacing={1}>
                <Text fontSize="2xl" fontWeight="bold">
                  {user?.full_name}
                </Text>
                <Text color="gray.600">{user?.email}</Text>
                <Text fontSize="sm" color="gray.500" textTransform="capitalize">
                  {user?.role}
                </Text>
              </VStack>
            </HStack>

            <Divider />

            <FormControl>
              <FormLabel>Full Name</FormLabel>
              <Input
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Your full name"
              />
            </FormControl>

            <FormControl>
              <FormLabel>Email</FormLabel>
              <Input value={user?.email} isReadOnly bg="gray.100" />
            </FormControl>

            <FormControl>
              <FormLabel>Organization ID</FormLabel>
              <Input value={user?.organization_id} isReadOnly bg="gray.100" />
            </FormControl>

            <Button
              colorScheme="blue"
              onClick={handleUpdateProfile}
              isLoading={isLoading}
            >
              Update Profile
            </Button>
          </VStack>
        </Box>

        <Box bg={cardBg} p={8} borderRadius="lg" shadow="md" borderWidth="1px">
          <VStack align="stretch" spacing={4}>
            <Heading size="md">Account Information</Heading>
            <HStack justify="space-between">
              <Text color="gray.600">Member Since</Text>
              <Text fontWeight="medium">
                {user?.created_at
                  ? new Date(user.created_at).toLocaleDateString()
                  : 'N/A'}
              </Text>
            </HStack>
            <HStack justify="space-between">
              <Text color="gray.600">Last Login</Text>
              <Text fontWeight="medium">
                {user?.last_login
                  ? new Date(user.last_login).toLocaleDateString()
                  : 'N/A'}
              </Text>
            </HStack>
            <HStack justify="space-between">
              <Text color="gray.600">Account Status</Text>
              <Text fontWeight="medium" color={user?.is_active ? 'green.500' : 'red.500'}>
                {user?.is_active ? 'Active' : 'Inactive'}
              </Text>
            </HStack>
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
};

export default Profile;

