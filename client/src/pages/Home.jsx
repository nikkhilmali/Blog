import React, { useState } from 'react';
import { useQuery, useMutation, gql } from '@apollo/client';
import { motion } from 'framer-motion';
import { FiPlus } from 'react-icons/fi';

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
      id
      like
      dislike
    }
  }
`;

const ADD_BLOG_MUTATION = gql`
  mutation AddBlog($username: String!, $content: String!) {
    addBlog(username: $username, content: $content) {
      id
      username
      content
      like
      dislike
      createdAt
    }
  }
`;

function Home() {
  const { loading, error, data, refetch } = useQuery(BLOG_QUERY);
  const [likeOrDislike] = useMutation(LIKE_DISLIKE_MUTATION);
  const [addBlog] = useMutation(ADD_BLOG_MUTATION);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [username, setUsername] = useState('');
  const [content, setContent] = useState('');

  const handleReaction = async (blogId, field) => {
    try {
      await likeOrDislike({ variables: { blogId, value: 1, field } });
      refetch();
    } catch (err) {
      console.error('Error updating reaction:', err);
    }
  };

  const handleAddBlog = async () => {
    if (!username || !content) return;
    try {
      await addBlog({ variables: { username, content } });
      refetch();
      setIsModalOpen(false);
      setUsername('');
      setContent('');
    } catch (err) {
      console.error('Error adding blog:', err);
    }
  };

  if (loading) return <p className="text-center text-gray-500">Loading...</p>;
  if (error) return <p className="text-center text-red-500">Error loading blogs.</p>;

  return (
    <div className="min-h-screen bg-gray-100 p-8 relative">
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

      {/* Floating Button */}
      <button
        onClick={() => setIsModalOpen(true)}
        className="fixed bottom-8 right-8 bg-blue-500 text-white p-4 rounded-full shadow-lg hover:bg-blue-600 transition"
      >
        <FiPlus size={24} />
      </button>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h3 className="text-lg font-semibold mb-4">New Blog Post</h3>
            <input
              type="text"
              placeholder="Your Name"
              className="w-full p-2 border rounded mb-2"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <textarea
              placeholder="Write your blog..."
              className="w-full p-2 border rounded mb-2"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setIsModalOpen(false)}
                className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
              >
                Cancel
              </button>
              <button
                onClick={handleAddBlog}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Post
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;
