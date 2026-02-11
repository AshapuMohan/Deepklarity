import React, { useEffect, useState } from 'react';
import { getQuizHistory, getQuizDetails } from '../api';
import QuizModal from './QuizModal';

const QuizHistory = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedQuiz, setSelectedQuiz] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const data = await getQuizHistory();
            setHistory(data);
        } catch (error) {
            console.error("Failed to load history", error);
        } finally {
            setLoading(false);
        }
    };

    const handleDetailsClick = async (id) => {
        try {
            const quiz = await getQuizDetails(id);
            setSelectedQuiz(quiz);
            setIsModalOpen(true);
        } catch (error) {
            console.error("Failed to load quiz details", error);
        }
    };

    if (loading) return <div className="text-center py-10">Loading history...</div>;

    return (
        <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">Quiz History</h2>
            {history.length === 0 ? (
                <p className="text-gray-500">No quizzes generated yet.</p>
            ) : (
                <div className="overflow-x-auto">
                    <table className="min-w-full leading-normal">
                        <thead>
                            <tr>
                                <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    ID
                                </th>
                                <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Title
                                </th>
                                <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    URL
                                </th>
                                <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                    Action
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((quiz) => (
                                <tr key={quiz.id}>
                                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                                        {quiz.id}
                                    </td>
                                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm font-medium">
                                        {quiz.title}
                                    </td>
                                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm text-blue-500 truncate max-w-xs">
                                        <a href={quiz.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
                                            {quiz.url}
                                        </a>
                                    </td>
                                    <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                                        <button
                                            onClick={() => handleDetailsClick(quiz.id)}
                                            className="bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-700 transition"
                                        >
                                            Details
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            <QuizModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                quiz={selectedQuiz}
            />
        </div>
    );
};

export default QuizHistory;
