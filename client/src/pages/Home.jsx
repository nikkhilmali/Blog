import React from 'react';
import { useQuery, useMutation, gql } from '@apollo/client';
import { motion } from 'framer-motion';

const BLOG_QUERY = gql`
  query Blog {
    blog {
      username
      content
      id
      like
      dislike
      createdAt
    }
  }
`;

const LIKE_DISLIKE_MUTATION = gql`
  mutation LikeOrDislike($blogId: String!, $value: Int!, $field: String!) {
    likeOrDislike(blogId: $blogId, value: $value, field: $field) {
      userId
      content
      id
      like
      dislike
      createdAt
    }
  }
`;

function Home() {
  const { loading, error, data, refetch } = useQuery(BLOG_QUERY);
  const [likeOrDislike] = useMutation(LIKE_DISLIKE_MUTATION);

  const handleReaction = async (blogId, field) => {
    try {
      await likeOrDislike({
        variables: { blogId, value: 1, field },
      });
      refetch(); // Refresh data after mutation
    } catch (err) {
      console.error('Error updating reaction:', err);
    }
  };

  if (loading) return <p className="text-center text-gray-500">Loading...</p>;
  if (error) return <p className="text-center text-red-500">Error loading blogs.</p>;

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">Latest Blogs</h2>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {data.blog.map((post) => (
          <motion.div
            key={post.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
          >
            <h3 className="text-xl font-semibold text-gray-800">{post.username}</h3>
            <p className="text-gray-600 mt-2">{post.content}</p>
            <div className="flex justify-between items-center mt-4 text-sm text-gray-500">
              <span>{new Date(post.createdAt).toLocaleDateString()}</span>
              <div className="flex gap-4">
                <button
                  onClick={() => handleReaction(post.id, 'like')}
                  className="text-green-500 hover:text-green-600"
                >
                  👍 {post.like}
                </button>
                <button
                  onClick={() => handleReaction(post.id, 'dislike')}
                  className="text-red-500 hover:text-red-600"
                >
                  👎 {post.dislike}
                </button>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

export default Home;
