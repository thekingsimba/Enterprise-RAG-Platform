import React from 'react';
import {
  Box,
  Flex,
  Button,
  HStack,
  IconButton,
  useDisclosure,
  Drawer,
  DrawerBody,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  VStack,
  Text,
  Avatar,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
  useColorModeValue,
} from '@chakra-ui/react';
import { HamburgerIcon } from '@chakra-ui/icons';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, logout, isAuthenticated } = useAuth();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const navigate = useNavigate();

  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { label: 'Dashboard', path: '/' },
    { label: 'Documents', path: '/documents' },
    { label: 'Chat', path: '/chat' },
  ];

  if (user?.role === 'admin') {
    navItems.push({ label: 'Admin', path: '/admin' });
  }

  if (!isAuthenticated) {
    return <Box>{children}</Box>;
  }

  return (
    <Box minH="100vh" bg={useColorModeValue('gray.50', 'gray.900')}>
      {/* Top Navigation */}
      <Box
        bg={bgColor}
        borderBottom="1px"
        borderColor={borderColor}
        px={4}
        position="sticky"
        top={0}
        zIndex={10}
      >
        <Flex h={16} alignItems="center" justifyContent="space-between">
          <HStack spacing={8} alignItems="center">
            <IconButton
              size="md"
              icon={<HamburgerIcon />}
              aria-label="Open Menu"
              display={{ md: 'none' }}
              onClick={onOpen}
            />
            <Text fontSize="xl" fontWeight="bold" color="blue.500">
              RAG Platform
            </Text>
            <HStack as="nav" spacing={4} display={{ base: 'none', md: 'flex' }}>
              {navItems.map((item) => (
                <Button
                  key={item.path}
                  as={Link}
                  to={item.path}
                  variant="ghost"
                >
                  {item.label}
                </Button>
              ))}
            </HStack>
          </HStack>
          <Flex alignItems="center">
            <Menu>
              <MenuButton
                as={Button}
                rounded="full"
                variant="link"
                cursor="pointer"
                minW={0}
              >
                <HStack>
                  <Avatar size="sm" name={user?.full_name} />
                  <VStack
                    display={{ base: 'none', md: 'flex' }}
                    alignItems="flex-start"
                    spacing="1px"
                    ml="2"
                  >
                    <Text fontSize="sm">{user?.full_name}</Text>
                    <Text fontSize="xs" color="gray.600">
                      {user?.role}
                    </Text>
                  </VStack>
                </HStack>
              </MenuButton>
              <MenuList>
                <MenuItem as={Link} to="/profile">
                  Profile
                </MenuItem>
                <MenuItem as={Link} to="/settings">
                  Settings
                </MenuItem>
                <MenuDivider />
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </MenuList>
            </Menu>
          </Flex>
        </Flex>
      </Box>

      {/* Mobile Navigation Drawer */}
      <Drawer isOpen={isOpen} placement="left" onClose={onClose}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader>Menu</DrawerHeader>
          <DrawerBody>
            <VStack align="stretch" spacing={2}>
              {navItems.map((item) => (
                <Button
                  key={item.path}
                  as={Link}
                  to={item.path}
                  variant="ghost"
                  justifyContent="flex-start"
                  onClick={onClose}
                >
                  {item.label}
                </Button>
              ))}
            </VStack>
          </DrawerBody>
        </DrawerContent>
      </Drawer>

      {/* Main Content */}
      <Box as="main" p={4}>
        {children}
      </Box>
    </Box>
  );
};

export default Layout;

