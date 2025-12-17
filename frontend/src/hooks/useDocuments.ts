import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { documentsService } from '@/services/documents.service';
import { useToast } from '@chakra-ui/react';

export const useDocuments = (skip = 0, limit = 20) => {
  return useQuery({
    queryKey: ['documents', skip, limit],
    queryFn: () => documentsService.getDocuments(skip, limit),
  });
};

export const useDocument = (id: string) => {
  return useQuery({
    queryKey: ['document', id],
    queryFn: () => documentsService.getDocument(id),
    enabled: !!id,
  });
};

export const useUploadDocument = () => {
  const queryClient = useQueryClient();
  const toast = useToast();

  return useMutation({
    mutationFn: ({ file, title, description }: { file: File; title?: string; description?: string }) =>
      documentsService.uploadDocument(file, title, description),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
      toast({
        title: 'Document uploaded successfully',
        status: 'success',
        duration: 3000,
      });
    },
    onError: (error: any) => {
      toast({
        title: 'Upload failed',
        description: error.response?.data?.detail || 'Failed to upload document',
        status: 'error',
        duration: 5000,
      });
    },
  });
};

export const useUpdateDocument = () => {
  const queryClient = useQueryClient();
  const toast = useToast();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) =>
      documentsService.updateDocument(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
      toast({
        title: 'Document updated',
        status: 'success',
        duration: 3000,
      });
    },
  });
};

export const useDeleteDocument = () => {
  const queryClient = useQueryClient();
  const toast = useToast();

  return useMutation({
    mutationFn: (id: string) => documentsService.deleteDocument(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
      toast({
        title: 'Document deleted',
        status: 'success',
        duration: 3000,
      });
    },
  });
};

