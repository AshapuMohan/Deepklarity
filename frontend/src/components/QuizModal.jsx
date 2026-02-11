import React from 'react';

const QuizModal = ({ isOpen, onClose, quiz }) => {
    if (!isOpen || !quiz) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
            <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
                <div className="flex justify-between items-center p-6 border-b">
                    <h2 className="text-2xl font-bold text-gray-800">{quiz.title}</h2>
                    <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <div className="p-6 space-y-6">
                    {/* Summary */}
                    <section>
                        <h3 className="text-lg font-semibold text-gray-700 mb-2">Summary</h3>
                        <p className="text-gray-600 leading-relaxed">{quiz.summary}</p>
                    </section>

                    {/* Key Entities */}
                    <section>
                        <h3 className="text-lg font-semibold text-gray-700 mb-2">Key Entities</h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div className="bg-blue-50 p-3 rounded">
                                <h4 className="font-medium text-blue-700 mb-1">People</h4>
                                <ul className="list-disc list-inside text-sm text-gray-600">
                                    {quiz.key_entities?.people?.map((item, idx) => (
                                        <li key={idx}>{item}</li>
                                    )) || <li>None found</li>}
                                </ul>
                            </div>
                            <div className="bg-green-50 p-3 rounded">
                                <h4 className="font-medium text-green-700 mb-1">Organizations</h4>
                                <ul className="list-disc list-inside text-sm text-gray-600">
                                    {quiz.key_entities?.organizations?.map((item, idx) => (
                                        <li key={idx}>{item}</li>
                                    )) || <li>None found</li>}
                                </ul>
                            </div>
                            <div className="bg-yellow-50 p-3 rounded">
                                <h4 className="font-medium text-yellow-700 mb-1">Locations</h4>
                                <ul className="list-disc list-inside text-sm text-gray-600">
                                    {quiz.key_entities?.locations?.map((item, idx) => (
                                        <li key={idx}>{item}</li>
                                    )) || <li>None found</li>}
                                </ul>
                            </div>
                        </div>
                    </section>

                    {/* Quiz Questions */}
                    <section>
                        <h3 className="text-lg font-semibold text-gray-700 mb-4">Quiz Questions</h3>
                        <div className="space-y-6">
                            {quiz.quiz?.map((q, idx) => (
                                <div key={idx} className="border rounded-lg p-4 bg-gray-50">
                                    <div className="flex justify-between items-start mb-2">
                                        <p className="font-medium text-gray-800 text-lg">{idx + 1}. {q.question}</p>
                                        <span className={`text-xs px-2 py-1 rounded font-bold uppercase ${q.difficulty === 'easy' ? 'bg-green-200 text-green-800' :
                                                q.difficulty === 'medium' ? 'bg-yellow-200 text-yellow-800' :
                                                    'bg-red-200 text-red-800'
                                            }`}>
                                            {q.difficulty}
                                        </span>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-3">
                                        {q.options.map((opt, optIdx) => (
                                            <div key={optIdx} className={`p-2 rounded border ${opt === q.answer ? 'bg-green-100 border-green-300' : 'bg-white border-gray-200'
                                                }`}>
                                                <span className="font-semibold mr-2">{String.fromCharCode(65 + optIdx)}.</span>
                                                {opt}
                                            </div>
                                        ))}
                                    </div>

                                    <div className="mt-3 text-sm text-gray-600 bg-blue-50 p-2 rounded">
                                        <span className="font-bold text-blue-700">Explanation:</span> {q.explanation}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* Related Topics */}
                    <section>
                        <h3 className="text-lg font-semibold text-gray-700 mb-2">Related Topics</h3>
                        <div className="flex flex-wrap gap-2">
                            {quiz.related_topics?.map((topic, idx) => (
                                <span key={idx} className="bg-gray-200 text-gray-700 px-3 py-1 rounded-full text-sm">
                                    {topic}
                                </span>
                            )) || <span>None found</span>}
                        </div>
                    </section>
                </div>

                <div className="p-6 border-t bg-gray-50 flex justify-end">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 transition"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
};

export default QuizModal;
