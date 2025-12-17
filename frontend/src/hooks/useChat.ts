import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { chatService } from '@/services/chat.service';
import { useToast } from '@chakra-ui/react';

export const useConversations = (skip = 0, limit = 20) => {
  return useQuery({
    queryKey: ['conversations', skip, limit],
    queryFn: () => chatService.getConversations(skip, limit),
  });
};

export const useConversation = (id: string) => {
  return useQuery({
    queryKey: ['conversation', id],
    queryFn: () => chatService.getConversation(id),
    enabled: !!id,
  });
};

export const useSendMessage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: chatService.sendMessage,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
      queryClient.invalidateQueries({ queryKey: ['conversation', data.conversation_id] });
    },
  });
};

export const useSendMessageWithWorkflow = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: chatService.sendMessageWithWorkflow,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
      queryClient.invalidateQueries({ queryKey: ['conversation', data.conversation_id] });
    },
  });
};

export const useDeleteConversation = () => {
  const queryClient = useQueryClient();
  const toast = useToast();

  return useMutation({
    mutationFn: (id: string) => chatService.deleteConversation(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
      toast({
        title: 'Conversation deleted',
        status: 'success',
        duration: 3000,
      });
    },
  });
};

